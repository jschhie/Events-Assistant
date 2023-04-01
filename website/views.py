from flask import Blueprint, render_template, request, redirect, flash
from flask_login import current_user, login_required
from . import db
from .models import Task
from .helpers import format_date, format_time # helper functions
from sqlalchemy import or_

import git # to create webhook for ```git push```

views = Blueprint('views', __name__)



# Create Webhook with GitHub: Deploy when master commits
@views.route('git_update', methods=['POST'])
def git_update():
    repo = git.Repo('./Events-Assistant')
    origin = repo.remotes.origin
    repo.create_head('master', 
                     origin.refs.master).set_tracking_branch(origin.refs.master).checkout()
    origin.pull()
    return '', 200



@views.route('/', methods=['POST', 'GET'])
@views.route('/home', methods=['POST', 'GET'])
@login_required
def home():
    if request.method == 'POST':
        # Search Bar
        if request.form['action'] == 'Search':
            user_query = request.form['Query']
            query_filter = request.form['QueryFilter']
            all_user_tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.bookmarked.desc(), Task.due_date_int, Task.time) # sort by priority, where 1 = bookmarked, 0 = unbookmarked
            if (query_filter != "Filter By..."):
                if (user_query):
                    results = all_user_tasks.filter(Task.content.contains(user_query)).filter(Task.status==query_filter).all()
                else:
                    # Search * all queries with query_filter only
                    results = all_user_tasks.filter(Task.status==query_filter).all()
            else: # No filter applied
                results = all_user_tasks.filter(Task.content.contains(user_query)).all()
            return render_template('home.html', user=current_user, tasks=results, isQuery=True)

        # Optionally delete all Completed and Cancelled Tasks
        if request.form['action'] == 'Clean Up':
            unwanted_tasks = Task.query.filter_by(user_id=current_user.id). \
                                                filter(or_(Task.status == 'Completed', \
                                                            Task.status == 'Cancelled')).all()
            for task in unwanted_tasks:
                db.session.delete(task)
                db.session.commit()
            flash('Deleted all Completed and Cancelled Items!', category='success')
            remaining_tasks = Task.query.filter_by(user_id=current_user.id). \
                                                    order_by(Task.bookmarked.desc(), Task.due_date_int, Task.time).all()
            return render_template('home.html', user=current_user, tasks=remaining_tasks, isQuery=False)
        
        elif request.form['action'] == "Create New":
            return redirect('/create')
    # default action: display all tasks 
    tasks = Task.query.filter_by(user_id=current_user.id). \
                                order_by(Task.bookmarked.desc(), Task.due_date_int, Task.time).all() 
    return render_template('home.html', user=current_user, tasks=tasks, isQuery=False)



@views.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    if request.method == 'POST':
        if request.form['action'] == 'Add Task':
            # Collect data from submitted form
            content = request.form['content']
            due_date_int = request.form['due_date']
            time = request.form['time']
            
            print("orginal time format: ", time)
            print("type: ", type(time))

            new_time = format_time(time)
            # Parse str object YYYY-MM-DD format, and convert into formatted str 
            if len(content.strip()) < 1:
                flash('Event details too short!', category='error')
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
                    flash('New event added!', category='success')
                    return redirect('/')
                except:
                    flash('Error in adding new event.', category='error')
        elif request.form['action'] == 'Return Home':
            flash('Returning Home!', category='success')
            return redirect('/')
    return render_template('create.html', user=current_user)



@views.route('/delete/<int:id>')
@login_required
def delete(id):
    task_to_delete = Task.query.get(id)
    try:
        if task_to_delete.user_id == current_user.id:
            # only owner of Task can delete their Tasks
            db.session.delete(task_to_delete)
            db.session.commit()
            flash('Event deleted!', category='success')
            return redirect('/') 
    except:
        flash('Error in deleting event.', category='error')



@views.route('/bookmark/<int:id>')
@login_required
def bookmark(id):
    saved_task = Task.query.get(id)
    try:
        if saved_task.user_id == current_user.id:
            # Unsave task, if already saved
            if saved_task.bookmarked == True:
                saved_task.bookmarked = False
                flash('Unsaved event', category='success')
            else: # Save task
                saved_task.bookmarked = True
                flash('Saved event!', category='success')
            db.session.commit()
            return redirect('/') 
    except:
        flash('Error in bookmarking event.', category='error')
        return redirect('/') 



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
                flash('Event updated!', category='success')
                return redirect('/')
            except:
                flash('Error in updating event.', category='error')
    else:
        return render_template('update.html', task=updated_task, user=current_user)