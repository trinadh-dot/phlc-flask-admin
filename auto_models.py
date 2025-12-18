"""
Automatic Database Table Reflection
This module automatically discovers and creates SQLAlchemy models for ALL tables in the database
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData

db = SQLAlchemy()


def reflect_all_tables(app):
    """
    Automatically reflect all tables from the database and create models
    Returns a dictionary of {table_name: Model} for all tables
    """
    with app.app_context():
        # Create metadata and reflect all tables
        metadata = MetaData()
        metadata.reflect(bind=db.engine)
        
        # Create automap base
        Base = automap_base(metadata=metadata)
        
        # Generate all model classes automatically
        Base.prepare()
        
        # Get all reflected models
        models = {}
        for table_name in metadata.tables.keys():
            # Get the model class for this table
            if hasattr(Base.classes, table_name):
                model = getattr(Base.classes, table_name)
                models[table_name] = model
                print(f"✓ Reflected table: {table_name}")
            else:
                # For tables with spaces or special characters, try different approaches
                # Create a class name from table name
                class_name = ''.join(word.capitalize() for word in table_name.replace('_', ' ').replace(' ', '_').split('_'))
                if hasattr(Base.classes, class_name):
                    model = getattr(Base.classes, class_name)
                    models[table_name] = model
                    print(f"✓ Reflected table: {table_name} (as {class_name})")
        
        return models, metadata
