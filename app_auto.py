from flask import Flask
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import MetaData, inspect
from config import Config
from auto_models import db, reflect_all_tables


# Custom Index View to pass menu to template
class CustomAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        # Pass menu items to template
        return self.render('admin/index.html', menu_items=self.admin._menu)


# Custom ModelView for better display
class UniversalModelView(ModelView):
    """
    Universal ModelView that provides enhanced features for all models
    """
    page_size = 50
    can_view_details = True
    can_export = True
    export_types = ['csv', 'xls']
    
    def render(self, template, **kwargs):
        """Override render to always pass menu_items to templates"""
        kwargs['menu_items'] = self.admin._menu
        return super(UniversalModelView, self).render(template, **kwargs)
        
    def __init__(self, model, session, name=None, **kwargs):
        # Auto-configure columns
        if not hasattr(self, 'column_list'):
            try:
                columns = [c.name for c in model.__table__.columns if c.name != 'id'][:10]
                if columns:
                    self.column_list = columns
            except:
                pass
        
        # Auto-configure searchable columns
        if not hasattr(self, 'column_searchable_list'):
            searchable = []
            try:
                for column in model.__table__.columns:
                    col_type = str(column.type).upper()
                    if any(t in col_type for t in ['TEXT', 'VARCHAR', 'CHAR', 'STRING']):
                        searchable.append(column.name)
                if searchable:
                    self.column_searchable_list = searchable[:5]
            except:
                pass
        
        # Auto-configure filters
        if not hasattr(self, 'column_filters'):
            filters = []
            try:
                for column in model.__table__.columns:
                    col_type = str(column.type).upper()
                    if any(t in col_type for t in ['DATE', 'TIMESTAMP', 'BOOLEAN', 'INTEGER', 'FLOAT', 'NUMERIC']):
                        filters.append(column.name)
                if filters:
                    self.column_filters = filters[:5]
            except:
                pass
        
        # Enable sorting on all columns
        try:
            self.column_sortable_list = [c.name for c in model.__table__.columns]
        except:
            pass
        
        # Use provided name or generate from model
        if name is None:
            name = model.__table__.name
        
        super(UniversalModelView, self).__init__(model, session, name=name, **kwargs)


def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    
    # Initialize Flask-Admin with custom index view
    admin = Admin(
        app,
        name='Flask Admin - Auto Discovery',
        template_mode='bootstrap4',
        base_template='admin/master.html',
        index_view=CustomAdminIndexView(name='Home', url='/admin')
    )
    
    # Automatically discover and register all database tables
    print("\n" + "="*70)
    print("🔍 Discovering all database tables...")
    print("="*70 + "\n")
    
    auto_register_all_tables(admin, app)
    
    @app.route('/')
    def index():
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Flask Admin Dashboard</title>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body {
                    font-family: 'Inter', sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                }
                .container {
                    background: white;
                    padding: 60px;
                    border-radius: 20px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    text-align: center;
                    max-width: 600px;
                }
                h1 {
                    color: #1e293b;
                    margin-bottom: 15px;
                    font-size: 36px;
                }
                p {
                    color: #64748b;
                    margin-bottom: 30px;
                    font-size: 18px;
                    line-height: 1.6;
                }
                .btn {
                    display: inline-block;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 15px 40px;
                    text-decoration: none;
                    border-radius: 10px;
                    font-size: 18px;
                    font-weight: 600;
                    transition: all 0.3s;
                    box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
                }
                .btn:hover {
                    transform: translateY(-3px);
                    box-shadow: 0 15px 35px rgba(102, 126, 234, 0.6);
                }
                .features {
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    gap: 20px;
                    margin-top: 40px;
                    text-align: left;
                }
                .feature {
                    background: #f8fafc;
                    padding: 20px;
                    border-radius: 10px;
                }
                .feature h3 {
                    color: #4f46e5;
                    margin-bottom: 8px;
                    font-size: 16px;
                }
                .feature p {
                    color: #64748b;
                    margin: 0;
                    font-size: 14px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎯 Flask Admin Dashboard</h1>
                <p>Welcome to your modern database administration panel with automatic table discovery!</p>
                <a href="/admin" class="btn">Open Admin Panel →</a>
                
                <div class="features">
                    <div class="feature">
                        <h3>🔍 Auto Discovery</h3>
                        <p>All tables discovered automatically</p>
                    </div>
                    <div class="feature">
                        <h3>📊 Modern UI</h3>
                        <p>Beautiful sidebar navigation</p>
                    </div>
                    <div class="feature">
                        <h3>⚡ Fast Search</h3>
                        <p>Quickly find any table</p>
                    </div>
                    <div class="feature">
                        <h3>💾 Export Data</h3>
                        <p>CSV and Excel exports</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        '''
    
    return app


def auto_register_all_tables(admin, app):
    """
    Automatically discover ALL tables from the database and register them
    """
    # System tables to exclude
    SYSTEM_TABLES = {
        'alembic_version',
        'auth_group',
        'auth_group_permissions',
        'auth_permission',
        'auth_user',
        'auth_user_groups',
        'auth_user_user_permissions',
        'django_admin_log',
        'django_content_type',
        'django_migrations',
        'django_session',
        'pg_stat_statements',
        'pg_stat_statements_info',
    }
    
    SYSTEM_PREFIXES = ('auth_', 'django_', 'pg_', 'sql_', 'alembic_', 'information_schema')
    
    with app.app_context():
        # Get all table names from database
        inspector = inspect(db.engine)
        all_tables = inspector.get_table_names()
        
        print(f"Found {len(all_tables)} tables in database\n")
        
        registered_count = 0
        skipped_count = 0
        
        for table_name in sorted(all_tables):
            # Skip system tables
            if table_name in SYSTEM_TABLES:
                print(f"⊘ Skipped system table: {table_name}")
                skipped_count += 1
                continue
            
            # Skip tables with system prefixes
            if table_name.startswith(SYSTEM_PREFIXES):
                print(f"⊘ Skipped system table: {table_name}")
                skipped_count += 1
                continue
            
            try:
                # Create a dynamic model for this table
                metadata = MetaData()
                metadata.reflect(bind=db.engine, only=[table_name])
                table = metadata.tables[table_name]
                
                # Check if table has primary key
                if not table.primary_key.columns:
                    print(f"⚠ Skipped {table_name}: No primary key found (cannot edit without PK)")
                    skipped_count += 1
                    continue
                
                # Create a model class dynamically
                class_name = ''.join(word.capitalize() for word in table_name.replace(' ', '_').split('_'))
                
                # Create the model class
                DynamicModel = type(
                    class_name,
                    (db.Model,),
                    {
                        '__table__': table,
                        '__tablename__': table_name,
                    }
                )
                
                # Register with Flask-Admin
                admin.add_view(
                    UniversalModelView(
                        DynamicModel,
                        db.session,
                        name=table_name,
                        endpoint=table_name.replace(' ', '_').replace('-', '_').replace('.', '_')
                    )
                )
                
                print(f"✓ Registered: {table_name}")
                registered_count += 1
                
            except Exception as e:
                print(f"✗ Failed to register {table_name}: {str(e)[:80]}")
                skipped_count += 1
        
        print(f"\n{'='*70}")
        print(f"✓ Successfully registered: {registered_count} tables")
        print(f"⊘ Skipped: {skipped_count} tables")
        print(f"{'='*70}")
        
        if skipped_count > 0:
            print(f"\n💡 Tip: Some tables were skipped because they lack primary keys.")
            print(f"   Tables without primary keys cannot be edited in Flask-Admin.")
            print(f"   To include them, add a primary key column to those tables.\n")


if __name__ == '__main__':
    app = create_app()
    
    print("\n" + "="*70)
    print("🚀 Flask Admin - Auto Discovery Mode")
    print("="*70)
    print("\n📍 Admin panel: http://localhost:5000/admin")
    print("📍 Main page: http://localhost:5000")
    print("\n💡 Press CTRL+C to stop the server\n")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
