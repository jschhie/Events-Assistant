from flask import Blueprint, render_template, request, redirect, flash
from flask_login import current_user, login_required
from . import db
from .models import Task
from .helpers import format_date, format_time # helper functions

views = Blueprint('views', __name__)

@views.route('/', methods=['POST', 'GET'])
@login_required
def home():
    if request.method == 'POST':
        # Collect data from submitted form
        content = request.form['content']
        due_date = request.form['due_date']
        time = request.form['time']        
        new_time = format_time(time)

        # Parse str object YYYY-MM-DD format, and convert into formatted str 
        if len(content.strip()) < 1:
            flash('Task is too short!', category='error')
        else:
            due_date = format_date(due_date) 
            try:
                new_task = Task(content=content, due_date=due_date, time=new_time, user_id=current_user.id)
                db.session.add(new_task)
                db.session.commit()
                flash('New task added!', category='success')
                return redirect('/') # redirect to Home page
            except:
                flash('Error in adding new task.', category='error')
    
    # default action: display all tasks 
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.due_date).all() 
    return render_template('home.html', user=current_user, tasks=tasks)



@views.route('/delete/<int:id>')
@login_required
def delete(id):
    task_to_delete = Task.query.get(id)
    try:
        if task_to_delete.user_id == current_user.id:
            # only owner of Task can delete their Tasks
            db.session.delete(task_to_delete)
            db.session.commit()
            flash('Task deleted!', category='success')
            return redirect('/') # redirect to Home Page
    except:
        flash('Error in deleting task.', category='error')



@views.route('/change-status/<int:id>')
@login_required
def change_status(id):
    user_task = Task.query.get(id)
    try:
        if user_task.user_id == current_user.id:
            if user_task.status == "Incomplete":
                user_task.status = "Complete"
            else:
                user_task.status = "Incomplete"
            db.session.commit()
            flash('Status updated!', category='success')
            return redirect('/')
    except:
        flash('Error in changing status', category='error')



@views.route('/update/<int:id>', methods=['POST', 'GET'])
@login_required
def update(id):
    updated_task = Task.query.get(id)
    if request.method == 'POST':
        # make sure owner only can update 
        if updated_task.user_id == current_user.id:
            updated_task.content = request.form['content']
            date_obj = request.form['due_date']
            updated_task.due_date = format_date(date_obj)
            if date_obj:
                time = request.form['time']
                updated_task.time = format_time(time)
            else:
                updated_task.time = '' # default time: unspecified/optional
            try:
                db.session.commit()
                flash('Task updated!', category='success')
                return redirect('/') # redirect to Home Page with updated task
            except:
                flash('Error in updating task.', category='error')
    else:
        return render_template('update.html', task=updated_task, user=current_user) # Remain on / display Update Task Page