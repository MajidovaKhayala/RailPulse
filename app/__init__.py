# Bu faylda yalnız bunlar olmalıdır:
from flask import Flask

def create_app():
    app = Flask(__name__)
    
    from app.routes import main_routes
    app.register_blueprint(main_routes)
    
    return app

# from flask import Flask

# def create_app():
#     app = Flask(__name__)
    
#     # Configuration
#     app.config['SECRET_KEY'] = 'your-secret-key'
    
#     # Import and register blueprints/routes
#     from app.routes import main_routes
#     app.register_blueprint(main_routes)
    
#     return app
