from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Create Flask extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Load configuration from config.py
    app.config.from_object('config.Config')
    
    # Initialize extensions
    db.init_app(app)  # Ensure SQLAlchemy is initialized with the Flask app
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    from authors_app.controllers.auth.auth_controller import auth
    app.register_blueprint(auth)
    # Additional blueprints can be registered here

    # Import models here to avoid circular import
    from authors_app.models.user import User
    from authors_app.models.company import Company
    from authors_app.models.book import Book

    # Routes
    @app.route('/')
    def home():
        return "Hello, world!"

    return app

# Ensure that the application is run only when this script is executed directly
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
