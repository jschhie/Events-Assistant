from flask import Blueprint, render_template, request, redirect, flash
from flask_login import current_user, login_required
from . import db
from .models import Task
from .helpers import format_date, format_time # helper functions
from sqlalchemy import or_

views = Blueprint('views', __name__)



@views.route('/', methods=['POST', 'GET'])
@login_required
def home():
    if request.method == 'POST':
        # Optionally hide Completed Tasks
        if request.form['action'] == 'Hide Completed Tasks':
            tasks = Task.query.filter_by(user_id=current_user.id).filter(Task.status != 'Completed').order_by(Task.due_date).all()
            flash('Completed Tasks Hidden!', category='success')
            return render_template('home.html', user=current_user, tasks=tasks)

        # Optionally delete all Completed and Cancelled Tasks
        if request.form['action'] == 'Clean Up':
            unwanted_tasks = Task.query.filter_by(user_id=current_user.id).filter(or_(Task.status == 'Completed', Task.status == 'Cancelled')).all()
            for task in unwanted_tasks:
                db.session.delete(task)
                db.session.commit()
            flash('Completed and Cancelled Tasks Deleted!', category='success')
            remaining_tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.due_date_int).all()
            return render_template('home.html', user=current_user, tasks=remaining_tasks)

        # Collect data from submitted form
        content = request.form['content']
        due_date_int = request.form['due_date']
        time = request.form['time']
        new_time = format_time(time)

        # Parse str object YYYY-MM-DD format, and convert into formatted str 
        if len(content.strip()) < 1:
            flash('Task is too short!', category='error')
        else:
            due_date = format_date(due_date_int) 
            try:
                new_task = Task(content=content, 
                                due_date=due_date, 
                                due_date_int=due_date_int,
                                time=new_time, 
                                user_id=current_user.id)
                db.session.add(new_task)
                db.session.commit()
                flash('New task added!', category='success')
                return redirect('/')
            except:
                flash('Error in adding new task.', category='error')

    # default action: display all tasks 
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.due_date_int, Task.time).all() 
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
            return redirect('/') 
    except:
        flash('Error in deleting task.', category='error')



@views.route('/update/<int:id>', methods=['POST', 'GET'])
@login_required
def update(id):
    updated_task = Task.query.get(id)
    if request.method == 'POST':
        if request.form['action'] == 'Return Home':
            flash('Update cancelled. Returning Home!', category='success')
            return redirect('/')

        # Otherwise Update Button submitted
        # and make sure owner only can update 
        if updated_task.user_id == current_user.id:
            updated_task.content = request.form['content']
            date_obj = request.form['due_date']
            updated_task.due_date = format_date(date_obj)
            updated_task.due_date_int = date_obj
            if date_obj:
                time = request.form['time']
                updated_task.time = format_time(time)
            else:
                updated_task.time = '' # default time: unspecified/optional
            updated_task.status = request.form.get('taskStatus')
            try:
                db.session.commit()
                flash('Task updated!', category='success')
                return redirect('/')
            except:
                flash('Error in updating task.', category='error')
    else:
        return render_template('update.html', task=updated_task, user=current_user) 
