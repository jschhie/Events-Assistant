from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "tasks_database.db"



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '2797cfdcad8dcc11d9f00ffbc5704bee'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    # register blueprints into app
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # create or retrieve existing DB
    from .models import Task, User
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
