# IMPORT FOR: FORMAT_TIME() AND FORMAT_DATE()
import calendar
import datetime

# IMPORT FOR: GET_GROUPS()
from . import db
from .models import User, Task, Group, GroupMember
from flask_login import current_user



def format_time(time) -> str:
    # Convert to str with AM, PM units
    new_time = ''
    if len(time) == 0:
        return new_time # Skip rest of code below, terminate early

    # Specific time given by user
    hour = int(time[:2])
    if hour >= 1 and hour < 10:
        new_time = time[1:] + ' AM' # remove leading 0
    elif hour == 10 or hour == 11:
        new_time = time + ' AM'
    elif hour == 12:
        new_time = time + ' PM'
    elif hour == 0:
        # convert 0 o clock to 12 o clock
        new_time = '12' + time[2:] + ' AM'
    else:
        # convert to regular 12 hour time
        result = hour - 12
        if result < 10:
            new_time = str(result)
        else:
            new_time = '1' + str(result - 10)
        new_time += time[2:] + ' PM'
    return new_time



def format_date(task_due_date) -> str:
    date_obj = None
    if task_due_date:
        # due date is given as YYYY-MM-DD format
        month_index = int(task_due_date[5:7]) # int
        month = calendar.month_name[month_index] # str
        day = task_due_date[8:] # str
        year = task_due_date[0:4] # str
        date_obj = datetime.date(int(year), month_index, int(day)) # date object
        day_of_week = calendar.day_name[date_obj.weekday()]
        task_due_date = day_of_week + ", " + month + " " + day + ", " + year
    else: # account for optional due dates
        task_due_date = None
    return task_due_date



def get_shared_groups_and_tasks() -> list:
    # get user's groups
    groups = Group.query.filter_by(user_id=current_user.id).all()

    # get user's shared groups (not owned by current_user)
    shared_groups = None
    shared_tasks = None
    matching_results = GroupMember.query.filter_by(user_id=current_user.id).all()
    if (matching_results):
        # At least one shared Group with current_user
        shared_groups = []
        shared_tasks = []
        for group_member in matching_results:
            # get matching groups 
            shared_group = Group.query.filter_by(id=group_member.group_id).first()
            print('Matching Shared Group: ', shared_group)
            shared_groups.append(shared_group)
            # Get all shared, grouped tasks 
            grouped_tasks = Task.query.filter_by(group_id=group_member.group_id).all()
            shared_tasks += grouped_tasks

    print("Groups Owned by current_user: ", groups)
    print("****")
    print("Shared Groups: ", shared_groups)
    print("========")
    print("Shared, Grouped Tasks", shared_tasks)

    return [groups, shared_groups, shared_tasks]



def find_restricted_tasks(shared_groups) -> list:
    restricted_tasks = [] # list of Task.id's associated with 'Viewer' access mode only
    if (shared_groups == None):
        return restricted_tasks # Skip loop below, return empty list
    
    for shared_group in shared_groups:
        matching_member = GroupMember.query.filter_by(group_id=shared_group.id).filter_by(user_id=current_user.id).first()
        if (not matching_member.is_editor):
            # Find all shared Tasks within that Group 
            matching_tasks = Task.query.filter_by(group_id=shared_group.id).all()
            for task in matching_tasks:
                restricted_tasks.append(task.id)
    return restricted_tasks
