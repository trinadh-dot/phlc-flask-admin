#!/usr/bin/env python
"""
Run Flask Admin with Automatic Table Discovery
This will automatically discover ALL tables in your database
"""
from app_auto import create_app

app = create_app()

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚀 Flask Admin - AUTO DISCOVERY MODE")
    print("="*70)
    print("\n✨ All database tables will be automatically discovered!")
    print("📍 Admin panel: http://localhost:5000/admin")
    print("📍 Main page: http://localhost:5000")
    print("\n💡 Press CTRL+C to stop the server\n")
    print("="*70 + "\n")
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )
