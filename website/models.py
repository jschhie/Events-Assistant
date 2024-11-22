from . import db
from flask_login import UserMixin



class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.String(30)) # formatted str date (ex: Tuesday, April 05, 2022)
    due_date_int = db.Column(db.String(20)) # YYYY-MM-DD str format 
    time = db.Column(db.String(20)) # str type, account for untimed tasks
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(30), default="Not Yet Started") # Other Statuses: In Progress, Completed, Cancelled
    bookmarked = db.Column(db.Boolean, default=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(150), unique=True) 
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    tasks = db.relationship('Task')



class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(30)) # title of group, ex: 'Homework'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Group owner/creator
    group_members = db.relationship('GroupMember') # applicable for Shared Groups



class GroupMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Group member (who is not the owner)
    username = db.Column(db.String(150)) 
    group_id =  db.Column(db.Integer, db.ForeignKey('group.id'))
    is_editor = db.Column(db.Boolean, default=True) # True: 'Editor' (WRITE) mode; Or, False: 'Viewer' (READ) mode