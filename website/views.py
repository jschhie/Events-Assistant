from flask import Blueprint, render_template, request, redirect, flash
from flask_login import current_user, login_required
from . import db
from .models import User, Task, Group, GroupMember
from .helpers import format_date, format_time, get_shared_groups_and_tasks # helper functions
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

    groups, shared_groups, shared_tasks = get_shared_groups_and_tasks() # returns a list of objects

    if request.method == 'POST':
        # Go to Group
        if request.form['action'] == 'View All':
            print('all groups!')
            pass
        elif 'Group' in request.form['action'] and request.form['action'] != "Add Group" and request.form['action'] != "New Group" and request.form['action'] != "Save Group" and request.form['action'] != "Leave Group":
            # get group id at the end of string
            group_id = request.form['action'].replace('Group','')
            group = Group.query.filter_by(id=group_id).first()
            
            # default action: display all tasks (owned by current_user)
            tasks = Task.query.filter_by(user_id=current_user.id). \
                                order_by(Task.bookmarked.desc(), Task.due_date_int, Task.time). \
                                filter_by(group_id=group_id).all()             

            if (shared_groups):
                # look through shared tasks for selected group
                for shared_group in shared_groups:
                    if (str(shared_group.id) == group_id):
                        print("selected group id is a shared group!")
                        grouped_shared_tasks = Task.query.filter_by(group_id=group_id). \
                                order_by(Task.bookmarked.desc(), Task.due_date_int, Task.time).all() 
                        return render_template('home.html', user=current_user, tasks=grouped_shared_tasks, isQuery=False, groups=groups+shared_groups, group_name=group.name, group=group)

                # Otherwise, user did not select a shared Group to view: Return all tasks
                print("did not select a shared group to view")
                return render_template('home.html', user=current_user, tasks=tasks, isQuery=False, groups=groups+shared_groups, group_name=group.name, group=group)
            else: # No groups shared with current user
                return render_template('home.html', user=current_user, tasks=tasks, isQuery=False, groups=groups, group_name=group.name, group=group)
        
        # Search Bar
        elif request.form['action'] == 'Search':
            user_query = request.form['Query']
            query_filter = request.form['QueryFilter']
            group_filter = request.form['GroupFilter']
            group = Group.query.filter_by(id=group_filter).first()
            
            all_user_tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.bookmarked.desc(), Task.due_date_int, Task.time) # sort by priority, where 1 = bookmarked, 0 = unbookmarked

            # Combine user Tasks (owned) and Group Tasks (shared)
            if (shared_groups and shared_tasks):
                groups += shared_groups
    
                filter_values = [shared_task_obj.id for shared_task_obj in shared_tasks]
                all_user_tasks = Task.query.filter_by(user_id=current_user.id). \
                                        union(Task.query.filter(Task.id.in_(filter_values))). \
                                        order_by(Task.bookmarked.desc(), Task.due_date_int, Task.time) # sort by priority, where 1 = bookmarked, 0 = unbookmarked

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
                return render_template('home.html', user=current_user, tasks=results, isQuery=True, groups=groups, group_name=group.name, group=group)
            except:
                return render_template('home.html', user=current_user, tasks=results, isQuery=True, groups=groups, group_name="All Groups", group=None)

        # Optionally delete all Completed and Cancelled Tasks
        if request.form['action'] == 'Clean Up':
            
            # check if any shared Tasks are 'Completed'  or 'Cancelled'
            if (shared_tasks):

                filter_values = [shared_task_obj.id for shared_task_obj in shared_tasks]
                all_user_tasks = Task.query.filter_by(user_id=current_user.id). \
                                        union(Task.query.filter(Task.id.in_(filter_values)))

                unwanted_tasks = all_user_tasks.filter(or_(Task.status == 'Completed', \
                                                        Task.status == 'Cancelled')).all()
            else:
                unwanted_tasks = Task.query.filter_by(user_id=current_user.id). \
                                            filter(or_(Task.status == 'Completed', \
                                                        Task.status == 'Cancelled')).all()
            for task in unwanted_tasks:
                db.session.delete(task)
                db.session.commit()
            flash('Deleted all Completed and Cancelled Items!', category='success')
            remaining_tasks = Task.query.filter_by(user_id=current_user.id). \
                                                    order_by(Task.bookmarked.desc(), Task.due_date_int, Task.time).all()
            return render_template('home.html', user=current_user, tasks=remaining_tasks, isQuery=False, group_name="All Groups", group=None)
        
        elif request.form['action'] == "Create New":
            return redirect('/create')
        elif request.form['action'] == "Add Group":
            return redirect('/create-group')
        elif request.form['action'] == "Save Group":
            group_member_name = request.form['GroupMemberName']
            access_mode = request.form['AccessModeDropdown']
            group_id = request.form['HiddenGroupId']
            if (group_member_name):
                # check if username exists in DB and not same as current_user
                added_user = User.query.filter_by(username=group_member_name).first()
                current_group = Group.query.filter_by(id=group_id).first()
                if (added_user):
                    if (added_user.id != current_user.id):
                        # Check if updating existing GroupMember: if so, update their access mode
                        all_group_members = current_group.group_members
                        matching_member = GroupMember.query.filter_by(group_id=group_id).filter_by(username=group_member_name).first()
                        if (matching_member):
                            # Check if Group owner wants to remove a GroupMember
                            if (access_mode == 'Remove'):
                                db.session.delete(matching_member)
                                db.session.commit()
                                flash('\'' + group_member_name + '\'' + ' was removed from your group!')
                            else:
                                matching_member.is_editor = True if access_mode == 'Editor' else False
                                db.session.commit()
                                flash('Updated access mode!')
                        else:
                            # Create new GroupMember and add to current Group
                            if (access_mode != 'Remove'):
                                if (access_mode == 'Editor'):
                                    new_group_member = GroupMember(user_id=added_user.id, username=group_member_name, group_id=group_id, is_editor=True) # Editor Mode
                                else: # 'Viewer' mode
                                    new_group_member = GroupMember(user_id=added_user.id, username=group_member_name, group_id=group_id, is_editor=False) # Viewer Mode
                                db.session.add(new_group_member)
                                db.session.commit()
                                flash('\'' + group_member_name + '\'' + ' was added to your group!')
                            else:
                                # User error: Removing a valid user from database, but user is not currently in shared Group
                                flash('Error:' + '\'' + group_member_name + '\'' + ' is not part of your Group!', category='error')
                        # Remain on current Group
                        tasks = Task.query.filter_by(user_id=current_user.id). \
                                order_by(Task.bookmarked.desc(), Task.due_date_int, Task.time). \
                                filter_by(group_id=group_id).all() 
                        return render_template('home.html', user=current_user, tasks=tasks, isQuery=False, groups=groups, group_name=current_group.name, group=current_group)
                    else:
                        flash('Cannot add yourself to your own group!', category='error')
                else:
                    flash('Group Member not found!', category='error')
            else:
                flash('Please enter a valid username!', category='error')
        elif request.form['action'] == "Leave Group":
            group_id = request.form['HiddenGroupId']
            group = Group.query.filter_by(id=group_id).first()
            
            # Delete GroupMember info from DB
            try:
                group_member = GroupMember.query.filter_by(user_id=current_user.id).filter_by(group_id=group.id).first()
                print(group_member, " found!")
                db.session.delete(group_member)
                db.session.commit()
                flash("Left Group: {.name}! Returning Home.".format(group), category='success')
                # force refresh shared_groups and shared_tasks after GroupMember removal
                groups, shared_groups, shared_tasks = get_shared_groups_and_tasks() # returns a list of objects
            except:
                flash('Error! Unable to leave group. Please try again.', category='error')
                return redirect('/')

    # default action: display all tasks 
    tasks = Task.query.filter_by(user_id=current_user.id). \
                                order_by(Task.bookmarked.desc(), Task.due_date_int, Task.time).all() 
    
    if (shared_groups and shared_tasks):
        groups += shared_groups
        tasks += shared_tasks

    return render_template('home.html', user=current_user, tasks=tasks, isQuery=False, groups=groups, group_name="All Groups", group=None)



@views.route('/create-group', methods=['POST', 'GET'])
@login_required
def create_group():
    #get user's groups
    #groups = Group.query.filter_by(user_id=current_user.id).all()
    groups, shared_groups, shared_tasks = get_shared_groups_and_tasks() # returns a list of objects
    if (shared_groups):
        groups += shared_groups

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
            return render_template('home.html', user=current_user, tasks=tasks, isQuery=False, groups=groups, group_name=group_name, group=None)

        elif request.form['action'] == 'New Group':
            groupname = request.form['groupname']
            # Check if groupname exists in DB
            if (groupname):
                # Account for shared Groups with duplicate name
                if (shared_groups):
                    filter_values = [shared_group_obj.id for shared_group_obj in shared_groups]
                    group = Group.query.filter_by(name=groupname).filter_by(user_id=current_user.id). \
                                union(Group.query.filter_by(name=groupname).filter(Group.id.in_(filter_values))).first()
                else:
                    # No shared Groups
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
    
    #get user's groups
    #groups = Group.query.filter_by(user_id=current_user.id).all()
    
    return render_template('create-group.html', user=current_user, groups=groups)



@views.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    #get user's groups
    #groups = Group.query.filter_by(user_id=current_user.id).all()
    groups, shared_groups, shared_tasks = get_shared_groups_and_tasks() # returns a list of objects
    if (shared_groups):
        groups += shared_groups

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
    
    #get user's groups
    #groups = Group.query.filter_by(user_id=current_user.id).all()
    return render_template('create.html', user=current_user, groups=groups)



@views.route('/delete/<int:id>')
@login_required
def delete(id):
    task_to_delete = Task.query.get(id)

    # Account for editor_mode == True for Group Tasks (shared)
    is_owner =  False # default
    is_editor = True # default
    if (task_to_delete.user_id == current_user.id):
        is_owner = True
        is_editor = False

    try:
        if (is_owner or is_editor):
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

    # Account for editor_mode == True for Group Tasks (shared)
    is_owner =  False # default
    is_editor = True # default
    if (saved_task.user_id == current_user.id):
        is_owner = True
        is_editor = False

    try:
        if (is_owner or is_editor):
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
    #get user's groups
    #groups = Group.query.filter_by(user_id=current_user.id).all()
    groups, shared_groups, shared_tasks = get_shared_groups_and_tasks() # returns a list of objects
    if (shared_groups):
        groups += shared_groups

    updated_task = Task.query.get(id)

    if request.method == 'POST':
        # Go to Group
        if request.form['action'] == 'View All':
            tasks = Task.query.filter_by(user_id=current_user.id). \
                                order_by(Task.bookmarked.desc(), Task.due_date_int, Task.time).all() 
            tasks += shared_tasks
            return render_template('home.html', user=current_user, tasks=tasks, isQuery=False, groups=groups, group_name="All Groups")
        
        elif 'Group' in request.form['action']:
            # get group id at the end of string
            group_id = request.form['action'].replace('Group','')
            group = Group.query.filter_by(id=group_id).first()
            tasks = Task.query.filter_by(user_id=current_user.id). \
                                order_by(Task.bookmarked.desc(), Task.due_date_int, Task.time). \
                                filter_by(group_id=group_id).all() 
            tasks += shared_tasks
            return render_template('home.html', user=current_user, tasks=tasks, isQuery=False, groups=groups, group_name=group.name)
        
        elif request.form['action'] == 'Return Home':
            flash('Update cancelled. Returning Home!', category='success')
            return redirect('/')

        # Otherwise Update Button submitted
        # and make sure owner only can update 

        # Account for editor_mode == True for Group Tasks (shared)
        is_owner =  False # default
        if (updated_task.user_id == current_user.id):
            is_owner = True

        is_shared_editor = False # default
        if (shared_groups):
            for shared_group in shared_groups:
                if (updated_task.group_id == shared_group.id):
                    is_shared_editor = True
                    is_owner = False

        if (is_owner or is_shared_editor):
            # Update Group: Only for Group owner 
            if (is_owner):
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
        #get user's groups
        #groups = Group.query.filter_by(user_id=current_user.id).all()
        return render_template('update.html', task=updated_task, user=current_user, groups=groups)