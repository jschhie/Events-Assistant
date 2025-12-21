from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from os import path, environ
from dotenv import load_dotenv

from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "tasks_database.db"



def create_app():
    app = Flask(__name__)

    # Get absolute path of current file (for server & local dev)
    current_dir = path.abspath(path.dirname(__file__))
    
    project_root = path.dirname(current_dir)
    env_path = path.join(project_root, '.env')
    load_dotenv(env_path)
    
    # Fetch Flask secret key from .env var
    # (To enable flashed msgs)
    app.config['SECRET_KEY'] = environ.get('FLASK_SECRET_KEY', 'dev-key-for-local-use-only')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    # register blueprints into app
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # create or retrieve existing DB
    from .models import Task, User, Group, GroupMember
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # if not logged in 
    login_manager.init_app(app)
    
    @login_manager.user_loader 
    def load_user(id):
        return User.query.get(int(id))

    return app



def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
