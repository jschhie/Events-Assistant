from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "tasks_database.db"



def create_app():
    """ create flask web app, connect to DB, and 
    register blueprints into app """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'some secret key here'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    # register blueprints into app
    from .views import views
    from .auth import auth

    # create or retrieve existing database
    from .models import Task
    create_database(app)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    return app



def create_database(app):
    """ check if the database instance has already been made """
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)