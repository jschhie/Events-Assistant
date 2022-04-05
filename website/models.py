from . import db
from flask_login import UserMixin



class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    # Longest possible str value for due_date: Wednesday,_September_10,_20XX = 9+1+1+9+1+2+1+1+4 = 29 chars
    due_date = db.Column(db.String(30)) # formats dates as DayOfWeek, Month DD, YYYY instead of specifying db.Column(db.Date)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(150), unique=True) 
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    tasks = db.relationship('Task')