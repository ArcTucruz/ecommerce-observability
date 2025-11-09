import os
from app import create_app

# Create Flask app
app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    
    print(f"🚀 Starting E-commerce API on port {port}...")
    print(f"📊 Database: {app.config['SQLALCHEMY_DATABASE_URI'].split('://')[0]}")
    print(f"💚 Health check: http://localhost:{port}/health")
    print(f"🌐 Frontend: http://localhost:{port}/")
    
    app.run(host='0.0.0.0', port=port, debug=debug)


#**This the start of the application!**


## ✅ BACKEND COMPLETE! 

#ecommerce-app/
#├── venv/                    ✅
#├── app/
#│   ├── __init__.py         ✅
#│   ├── models/             ✅ (4 model files)
#│   ├── services/           ✅ (4 service files)
#│   ├── routes/             ✅ (4 route files)
#│   └── utils/              ✅ (logger)
#├── static/                  (next step)
#├── .env                     ✅
#├── requirements.txt         ✅
#└── run.py                   ✅