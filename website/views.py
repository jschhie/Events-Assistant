from flask import Blueprint, render_template, request, redirect
from flask_login import current_user, login_required
from . import db
from .models import Task

views = Blueprint('views', __name__)

@views.route('/', methods=['POST', 'GET'])
@login_required
def home():
    if request.method == 'POST':
        task_content = request.form['task']
        if len(task_content) < 1:
            print('too short')
        else:
            new_task = Task(content=task_content)
            try:
                db.session.add(new_task)
                db.session.commit()
                print('new task added')
                print(task_content)
                return redirect('/') # redirect to home page
            except:
                print('error in adding new task')
    
    # in case of errors, failure
    tasks = Task.query.order_by(Task.due_date).all() # order by due date
    return render_template('home.html', user=current_user)