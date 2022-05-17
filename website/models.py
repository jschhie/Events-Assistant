from . import db
from flask_login import UserMixin



class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.String(30)) # formatted str date (ex: Tuesday, April 05, 2022)
    time = db.Column(db.String(20)) # str type, account for untimed tasks
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(30), default="Not Yet Started") # Statuses: Not Yet Started, In Progress, Completed, Cancelled


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(150), unique=True) 
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    tasks = db.relationship('Task')
