import calendar
import datetime

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
        # due date is given as YYYY-MM-DDD format
        month_index = int(task_due_date[5:7])
        month = calendar.month_name[month_index]
        day = task_due_date[8:]
        year = task_due_date[0:4]
        date_obj = datetime.date(int(year), month_index, int(day)) # date object
        day_of_week = calendar.day_name[date_obj.weekday()]
        task_due_date = day_of_week + ", " + month + " " + day + ", " + year
    else: # account for optional due dates
        task_due_date = None
    return task_due_date
