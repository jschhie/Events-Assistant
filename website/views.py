import datetime
import calendar
from flask import Blueprint, render_template, request, redirect
from flask_login import current_user, login_required
from . import db
from .models import Task

views = Blueprint('views', __name__)

@views.route('/', methods=['POST', 'GET'])
@login_required
def home():
    if request.method == 'POST':
        task_content = request.form['content']
        task_due_date = request.form['due_date']
        # Parse str object YYYY-MM-DD format, and convert into formatted str 
        if len(task_content.strip()) < 1:
            print('too short!!!!')
        else:
            task_due_date = format_date(task_due_date)
            try:
                new_task = Task(content=task_content, due_date=task_due_date, user_id=current_user.id) # added user_id arg
                db.session.add(new_task)
                db.session.commit()
                print('new task added with due date')
                return redirect('/') # redirect to home page
            except:
                print('error in adding new task')
    
    # default action: display all tasks in order of due date
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.due_date).all() # order by due date
    return render_template('home.html', user=current_user) #, tasks=tasks)



def format_date(task_due_date) -> str:
    if task_due_date:
        # due date is given as YYYY-MM-DDD format
        month_index = int(task_due_date[5:7]) # int
        month = calendar.month_name[month_index] # str
        day = task_due_date[8:] # str
        year = task_due_date[0:4] # str
        date_obj = datetime.date(int(year), month_index, int(day)) # date object
        day_of_week = calendar.day_name[date_obj.weekday()] # use date.weekday() method to get MONTH as str
        task_due_date = day_of_week + ", " + month + " " + day + ", " + year
    else: 
        # account for optional due dates: task_due_date is empty
        task_due_date = None
    return task_due_date