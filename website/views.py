import datetime
import calendar
from nis import cat
#from socket import CAN_RAW
from flask import Blueprint, render_template, request, redirect, flash
from flask_login import current_user, login_required
from . import db
from .models import Task

views = Blueprint('views', __name__)

@views.route('/', methods=['POST', 'GET'])
@login_required
def home():
    if request.method == 'POST':
        content = request.form['content']
        due_date = request.form['due_date']
        time = request.form['time']
        
        # Convert to str with AM, PM units
        print("TIME::: ", time)
        new_time = ''
        if len(time):
            hour = int(time[:2])
            print("HOUR : ", hour)
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



def format_date(task_due_date):
    date_obj = None
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
            try:
                db.session.commit()
                flash('Task updated!', category='success')
                return redirect('/') # redirect to Home Page with updated task
            except:
                flash('Error in updating task.', category='error')
    else:
        return render_template('update.html', task=updated_task, user=current_user) # Remain on / display Update Task Page