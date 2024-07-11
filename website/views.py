from flask import Blueprint, render_template, request, redirect, flash
from flask_login import current_user, login_required
from . import db
from .models import Task, Group
from .helpers import format_date, format_time # helper functions
from sqlalchemy import or_

import git # to create webhook for ```git push```

views = Blueprint('views', __name__)


# update: Create webhook with github
@views.route('/git_update', methods=['POST'])
def git_update():
    if request.method == 'POST':
        repo = git.Repo('./Events-Assistant')
        origin = repo.remotes.origin
        origin.pull()
        return 'updated pythonanywhere successfully!!', 200
    else:
        return 'wrong event type!!', 400

'''
# Create Webhook with GitHub: Deploy when master commits
@views.route('git_update', methods=['POST'])
def git_update():
    repo = git.Repo('./Events-Assistant')
    origin = repo.remotes.origin
    repo.create_head('master',
                     origin.refs.master).set_tracking_branch(origin.refs.master).checkout()
    origin.pull()
    return '', 200
'''

'''
@views.route('/groups-<string:groupname>', methods=['POST', 'GET'])
@login_required
def groups(groupname):
    # get all user's groups
    # replace %20 with whitespace
    print(groupname)

    groups = Group.query.filter_by(user_id=current_user.id).all()

    tasks = Task.query.filter_by(user_id=current_user.id). \
            order_by(Task.bookmarked.desc(), Task.due_date_int, Task.time).all()


    return render_template('home.html', user=current_user, tasks=tasks, isQuery=False, groups=groups, group_name=groupname)
'''


@views.route('/', methods=['POST', 'GET'])
@views.route('/home', methods=['POST', 'GET'])
@login_required
def home():
    # get user's groups
    groups = Group.query.filter_by(user_id=current_user.id).all()

    if request.method == 'POST':
        # Go to Group
        if request.form['action'] == 'View All':
            print('all groups!')
            pass
        elif 'Group' in request.form['action'] and request.form['action'] != "Add Group" and request.form['action'] != "New Group":
            # get group id at the end of string
            group_id = request.form['action'].replace('Group','')
            group = Group.query.filter_by(id=group_id).first()

            # default action: display all tasks
            tasks = Task.query.filter_by(user_id=current_user.id). \
                                order_by(Task.bookmarked.desc(), Task.due_date_int, Task.time). \
                                filter_by(group_id=group_id).all()

            #print(group.id)
            #print(group.name)

            return render_template('home.html', user=current_user, tasks=tasks, isQuery=False, groups=groups, group_name=group.name)
        # Search Bar
        elif request.form['action'] == 'Search':
            user_query = request.form['Query']
            query_filter = request.form['QueryFilter']
            group_filter = request.form['GroupFilter']
            group = Group.query.filter_by(id=group_filter).first()

            all_user_tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.bookmarked.desc(), Task.due_date_int, Task.time) # sort by priority, where 1 = bookmarked, 0 = unbookmarked

            if (query_filter != "Status" and group_filter != "Filter By..." and group_filter != "All"):
                if (user_query):
                    flash("Results for " + user_query + " that are " + query_filter + " and in " + group.name, category='success')
                    results = all_user_tasks.filter(Task.content.contains(user_query)).filter(Task.status==query_filter).filter(Task.group_id==group_filter).all()
                else:
                    # Search * all queries with query_filter and group_filter only
                    flash("Results for " + query_filter + ' items that are in ' + group.name, category='success')
                    results = all_user_tasks.filter(Task.status==query_filter).filter(Task.group_id==group_filter).all()

            elif (query_filter != "Status"):
                if (user_query):
                    flash("Results for " + user_query + " that are " + query_filter, category='success')
                    results = all_user_tasks.filter(Task.content.contains(user_query)).filter(Task.status==query_filter).all()
                else:
                    # Search * all queries with status_filter only
                    flash("Results for " + query_filter + " items", category='success')
                    results = all_user_tasks.filter(Task.status==query_filter).all()

            elif (group_filter != "Filter By..." and group_filter != "All"):
                if (user_query):
                    flash("Results for " + user_query + " that are in " + group.name, category='success')
                    results = all_user_tasks.filter(Task.content.contains(user_query)).filter(Task.group_id==group_filter).all()
                else:
                    # Search * all queries with group_filter only
                    flash("Results for items in " + group.name, category='success')
                    results = all_user_tasks.filter(Task.group_id==group_filter).all()

            else: # No filters applied
                flash("Results for " + user_query + " All Groups", category='success')
                results = all_user_tasks.filter(Task.content.contains(user_query)).all()

            try:
                return render_template('home.html', user=current_user, tasks=results, isQuery=True, groups=groups, group_name=group.name)
            except:
                return render_template('home.html', user=current_user, tasks=results, isQuery=True, groups=groups, group_name="All Groups")

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
            return render_template('home.html', user=current_user, tasks=remaining_tasks, isQuery=False, group_name="All Groups")

        elif request.form['action'] == "Create New":
            return redirect('/create')
        elif request.form['action'] == "Add Group":
            return redirect('/create-group')

    # default action: display all tasks
    tasks = Task.query.filter_by(user_id=current_user.id). \
                                order_by(Task.bookmarked.desc(), Task.due_date_int, Task.time).all()

    return render_template('home.html', user=current_user, tasks=tasks, isQuery=False, groups=groups, group_name="All Groups")



@views.route('/create-group', methods=['POST', 'GET'])
@login_required
def create_group():
    # get user's groups
    groups = Group.query.filter_by(user_id=current_user.id).all()
    if request.method == 'POST':
        # Go to Group
        if request.form['action'] == 'View All':
            tasks = Task.query.filter_by(user_id=current_user.id). \
                        order_by(Task.bookmarked.desc(), Task.due_date_int, Task.time).all()
            return render_template('home.html', user=current_user, tasks=tasks, isQuery=False, groups=groups, group_name="All Groups")

        elif 'Group' in request.form['action'] and request.form['action'] != "Add Group" and request.form['action'] != "New Group":
            # get group id at the end of string
            try:
                group_id = request.form['action'].replace('Group','')
                group = Group.query.filter_by(id=group_id).first()
                tasks = Task.query.filter_by(user_id=current_user.id). \
                                    order_by(Task.bookmarked.desc(), Task.due_date_int, Task.time). \
                                    filter_by(group_id=group_id).all()
                group_name = group.name
            except:
                group_id = request.form['action'].replace('Group','')
                print(group_id)
                tasks = Task.query.filter_by(user_id=current_user.id). \
                    order_by(Task.bookmarked.desc(), Task.due_date_int, Task.time).all()
                group_name = "All Groups"
            return render_template('home.html', user=current_user, tasks=tasks, isQuery=False, groups=groups, group_name=group_name)

        elif request.form['action'] == 'New Group':
            groupname = request.form['groupname']
            # Check if groupname exists in DB
            if (groupname):
                group = Group.query.filter_by(name=groupname).filter_by(user_id=current_user.id).first()
                if group:
                    flash(groupname + ' Group already exists! Please enter another Group name.', category='error')
                else:
                    new_group = Group(name=groupname, user_id=current_user.id)
                    db.session.add(new_group)
                    db.session.commit()
                    flash(groupname + ' Group Added!', category='success')
                    return redirect('/')
        elif request.form['action'] == 'Return Home':
            flash('Returning Home!', category='success')
            return redirect('/')

    # get user's groups
    groups = Group.query.filter_by(user_id=current_user.id).all()
    return render_template('create-group.html', user=current_user, groups=groups)



@views.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    # get user's groups
    groups = Group.query.filter_by(user_id=current_user.id).all()

    if request.method == 'POST':
        # Go to Group
        if request.form['action'] == 'View All':
            tasks = Task.query.filter_by(user_id=current_user.id). \
                        order_by(Task.bookmarked.desc(), Task.due_date_int, Task.time).all()
            return render_template('home.html', user=current_user, tasks=tasks, isQuery=False, groups=groups, group_name="All Groups")

        elif 'Group' in request.form['action']:
            # get group id at the end of string
            group_id = request.form['action'].replace('Group','')
            group = Group.query.filter_by(id=group_id).first()
            tasks = Task.query.filter_by(user_id=current_user.id). \
                                order_by(Task.bookmarked.desc(), Task.due_date_int, Task.time). \
                                filter_by(group_id=group_id).all()
            return render_template('home.html', user=current_user, tasks=tasks, isQuery=False, groups=groups, group_name=group.name)

        elif request.form['action'] == 'Add Task':
            # Collect data from submitted form
            content = request.form['content']
            due_date_int = request.form['due_date']
            time = request.form['time']

            #print("orginal time format: ", time)
            #print("type: ", type(time))

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
                                    user_id=current_user.id,
                                    group_id=None)
                    db.session.add(new_task)
                    db.session.commit()
                    flash('New event added!', category='success')
                    return redirect('/')
                except:
                    flash('Error in adding new event.', category='error')
        elif request.form['action'] == 'Return Home':
            flash('Returning Home!', category='success')
            return redirect('/')

    # get user's groups
    groups = Group.query.filter_by(user_id=current_user.id).all()
    return render_template('create.html', user=current_user, groups=groups)



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
    # get user's groups
    groups = Group.query.filter_by(user_id=current_user.id).all()

    updated_task = Task.query.get(id)

    if request.method == 'POST':
        # Go to Group
        if request.form['action'] == 'View All':
            tasks = Task.query.filter_by(user_id=current_user.id). \
                                order_by(Task.bookmarked.desc(), Task.due_date_int, Task.time).all()
            return render_template('home.html', user=current_user, tasks=tasks, isQuery=False, groups=groups, group_name="All Groups")

        elif 'Group' in request.form['action']:
            # get group id at the end of string
            group_id = request.form['action'].replace('Group','')
            group = Group.query.filter_by(id=group_id).first()
            tasks = Task.query.filter_by(user_id=current_user.id). \
                                order_by(Task.bookmarked.desc(), Task.due_date_int, Task.time). \
                                filter_by(group_id=group_id).all()
            return render_template('home.html', user=current_user, tasks=tasks, isQuery=False, groups=groups, group_name=group.name)

        elif request.form['action'] == 'Return Home':
            flash('Update cancelled. Returning Home!', category='success')
            return redirect('/')

        # Otherwise Update Button submitted
        # and make sure owner only can update
        if updated_task.user_id == current_user.id:

            # Update Group
            group_id = request.form['groupSelect']
            if group_id != "All":
                print(group_id)
                updated_task.group_id = group_id
            else:
                updated_task.group_id = None

            # Update Content, Due Date, Time
            updated_task.content = request.form['content']
            date_obj = request.form['due_date']
            updated_task.due_date = format_date(date_obj)
            updated_task.due_date_int = date_obj
            if date_obj:
                time = request.form['time']
                updated_task.time = format_time(time)
            else:
                updated_task.time = '' # default time: unspecified/optional
            # Update Status
            updated_task.status = request.form.get('taskStatus')
            try:
                db.session.commit()
                flash('Event updated!', category='success')
                return redirect('/')
            except:
                flash('Error in updating event.', category='error')
    else:
        # get user's groups
        groups = Group.query.filter_by(user_id=current_user.id).all()
        return render_template('update.html', task=updated_task, user=current_user, groups=groups)
