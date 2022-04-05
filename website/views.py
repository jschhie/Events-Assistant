import datetime
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
        # Parse str object YYYY-MM-DD format, and convert into date obj
        if len(task_content) < 1:
            print('too short')
        else:
            if task_due_date:
                # due date is specified, otherwise leave as None
                year = int(task_due_date[0:4])
                month = int(task_due_date[5:7])
                day = int(task_due_date[8:])
                task_due_date = datetime.date(year, month, day) 
            else: 
                # account for optional due dates: task_due_date is empty
                task_due_date = None
            try:
                new_task = Task(content=task_content, due_date=task_due_date)
                db.session.add(new_task)
                db.session.commit()
                print('new task added with due date')
                return redirect('/') # redirect to home page
            except:
                print('error in adding new task')
    
    # in case of errors, failure
    #tasks = Task.query.all() # display all of current user's tasks
    tasks = Task.query.order_by(Task.due_date).all() # order by due date
    return render_template('home.html', user=current_user, tasks=tasks)