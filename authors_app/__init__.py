from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

# Initialize extensions outside of create_app for better organization
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)

    # Load configuration from config.py
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # Register blueprints
    from authors_app.controllers.auth.auth_controller import auth
    app.register_blueprint(auth)
    #app.register_blueprint(Company)
    
    # Import models here to avoid circular import
    from authors_app.models.user import User
    from authors_app.models.company import Company
    from authors_app.models.book import Book

    # Routes
    @app.route('/')
    def home():
        return "Hello, world!"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
