from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



from app import config
from app.auth.routes import auth as auth_blueprint
from app.home.routes import home as home_blueprint
# from app.presence.routes import presence_bp as presence_blueprint

# db = SQLAlchemy()
migrate = Migrate()

def create_app():
    from .models import db  

    app = Flask(__name__)

    # Set the SQLAlchemy configurations
    app.config['SECRET_KEY'] = config.app_secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = config.sqlalchemy_database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for SQLAlchemy

    # Initialize the SQLAlchemy instance
    db.init_app(app)

    # Initialize Flask-Migrate
    migrate.init_app(app, db)

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(home_blueprint)
    # app.register_blueprint(presence_blueprint)

    return app

