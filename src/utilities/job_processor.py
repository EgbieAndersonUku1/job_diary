#####################################################################
# Author = Egbie Uku
#####################################################################

from datetime import datetime
from dateutil import relativedelta
import random

def _return_time_passed(start_date, start_time, finish_date, finish_time):
    """A wrapper function that returned the years, month, hours, days, minutes
    passed between two dates.
    """

    year1, month1, day1 = start_date.split('-')  
    year2, month2, day2 = finish_date.split('-') 
    hours1, minutes1 = start_time.split(':')
    hours2, minutes2 = finish_time.split(':')
    first_date = datetime(int(year1), int(month1), int(day1), int(hours1), int(minutes1))
    sec_date   = datetime(int(year2), int(month2), int(day2), int(hours2), int(minutes2))
    return relativedelta.relativedelta(sec_date, first_date)

def is_shift_confirmed(confirmation, job, func):
    """is_shift_confirmed(str, obj) -> returns(str)

    Checks whether the user's shift/job is confirmed.
    If confirmation is not made before the start of the shift
    then the module assumes that shift in question was cancelled
    and thus automatically deletes it from the database.

    :parameters
        - confirmation : either yes or no. Yes means the client/boss
                         confirmed the job/shift.
        - job: An object containg the user's job details.
        - func: Delete function deletes the row job in question.

    """
    if job.is_shift_confirmed.lower() == 'no' and is_shift_now(job):
        func(job.row_id[1:])
        return False
    return True

def is_shift_now(job):
    """is_shift_now(str, str, str, str) -> return(bool)

    Checks if the user shift has started. Returns True
    if it has or False if it has not.

    parameters:
       - job : An object that contains the job information.
       
    >>> is_shift_now(object(..))
    False
    >>> is_shift_now((object(..)))
    True
    """
    curr_time = datetime.now()
    start_hour = job.start_time.split(':')[0]
    start_mins = job.start_time.split(':')[1]
    end_hours =  job.finish_time.split(':')[0]
    end_mins =   job.finish_time.split(':')[1]
    shift_start_time = curr_time.replace(hour=int(start_hour), minute=int(start_mins))
    shift_end_time = curr_time.replace(hour=int(end_hours), minute=int(end_mins))
    return True if shift_start_time <= curr_time <= shift_end_time else False

def is_shift_over(job):
    """is_shift_over(obj) -> returns(bool)

    Checks whether the user current shift is over.
    Returns True if the shift is over and False if 
    it is not.

    parameters:
       - job : An object that contains the job information
               such as the job start date, start and finish
               time.

    >>> is_shift_over(object(..))
    False
    >>> is_shift_over(object(..))
    True
    """
    curr_time = datetime.now()
    start_time = job.finish_time.split(':')[0]
    finish_time = job.finish_time.split(':')[1]
    year, month, day = job.date.split('-')
    shift_end_time = curr_time.replace(year=int(year),
                                       month=int(month),
                                       day=int(day),
                                       hour=int(start_time), 
                                       minute=int(finish_time))
    return True if curr_time > shift_end_time else False

def when_is_shift_starting(start_date, start_time):
    """when_is_shift_starting(str, str) -> returns(str)

    Takes the date the job is starting along with its start
    time and returns how long it till the job starts.

    :parameters
        - start_date : The date the job is starting.
        - start_time : The time the job is starting.

    >>> job_date = '2016-12-09'
    >>> job_time = '13:30'
    >>> when_is_shift_starting(job_date, job_time)
    >>> 8 days, 22 hours, 58 minutes
    """
    date = datetime.utcnow()
    curr_date = '{}-{}-{}'.format(date.year, date.month, date.day)
    curr_time = '{}:{}'.format(date.hour, date.minute)
    shift_start = []
    date_obj = _return_time_passed(curr_date, curr_time, start_date, start_time)

    if date_obj.years:
        shift_start.append('{} years'.format(date_obj.years) if date_obj.years > 1 else '{} year'.format(date_obj.years))
    if date_obj.months:
        shift_start.append('{} months'.format(date_obj.months) if date_obj.months > 1 else '{} month'.format(date_obj.months))
    if date_obj.days:
        shift_start.append('{} days'.format(date_obj.days) if date_obj.days > 1 else '{} day'.format(date_obj.days))
    if date_obj.hours:
        shift_start.append('{} hours'.format(date_obj.hours) if date_obj.hours > 1 else '{} hour'.format(date_obj.hours))
    if date_obj.minutes:
        shift_start.append('{} minutes'.format(date_obj.minutes) if date_obj.minutes > 1 else '{} minute'.format(date_obj.minutes))
    
    time_elasped = ', '.join(shift_start)
    print time_elasped

    # if ',' not in time_elasped it means that countdown to start of the shift is 00:00
    # if '-' in time_elasped it means that shift has already began.
    return 'Shift/job in progress' if '-' in time_elasped or not ',' in time_elasped else time_elasped 
    
def get_hours_worked(start_date, start_time, finish_date, finish_time):
    """get_hours_worked(str, str, str, str) -> return(tuple)

    Takes a starting date and starting time as well as the
    ending date and a finishing time and returns the number of hours, 
    minutes that has elasped between the two.

    parameters 
      - start_date : The beginning date in the form of dd/mm/yy
      - end_date   : The ending date in the form of dd/mm/yy
      - start_time : The starting time in the form of hh:mm
      - finish_time: The starting time in the form of hh:mm
      - returns    : A tuple where the first element is the 
                     hours and second the minutes

    >>> get_hours_worked('1/1/2016', '9:23', 1/1/2016', '21:26')
    (12, 3)
    >>> get_hours_worked('1/1/2016', '9:23', 1/4/2016', '21:26')
    (83, 43)
    """
    
    difference = _return_time_passed(start_date, start_time, finish_date, finish_time)
    # if start date is not equal to the finish date it means that user
    # started on one day and finish on another day
    if start_date != finish_date:
        years, months, days = difference.years, difference.months, difference.days
        hours = 0
        if years > 0:
            hours += years * 8760
        if months > 0:
            hours += (730 * months)
        if days > 0:
            hours += days * 24           
        total_hours = difference.hours + hours # convert year, month or days to hours + regular hours
        return total_hours, difference.minutes
    return difference.hours, difference.minutes

def get_daily_rate(units, hourly_rate):
    """get_daily_rate(float, float) -> returns(float)

    Returns the daily rate.
    parameters: 
       - units       : The time in units
       - hourly_rate : The amount paid in hours
       - returns     : The total amount paid for the day
    """
    return round((units * float(hourly_rate)), 2)

def get_jobs(active_jobs, user_obj, session, curr_date):
    """get_job sorts the active jobs from the none active jobs

    parameters: 
        - active_jobs: flag that tells the function to only search for active jobs
        - user_obj   : user object module
        - session    : The session belonging to the user 
        - curr_date  : The current date
        - returns    : a tuple of lists where the first element is 
                       an object, second is the total pay,
                       sum of hours worked and a list of 
                       jobs worked.
    """
    user = user_obj(session['username'], _id=session['user_id'])
    total_pay, total_hrs, worked_jobs = [], [], []

    if active_jobs:
        jobs = user.get_by_user_id(sort_by=1) # sort job by ascending ldest active job first
    else:
        jobs = user.get_by_user_id()  # sort job in descending order newest first

    def get_jobs_helper(daily_rate, hrs, job):
        """returns the daily rate and the hours worked for the processed jobs"""
        total_pay.append(float(job.daily_rate))
        total_hrs.append(float(job._hours))
        worked_jobs.append(job)

    # sort the job based on whether the jobs are active
    for job in jobs:
        if not active_jobs:
            # if the shift day is less than the current day 
            # it means the shift has already been worked
            if datetime.strptime(job.date, "%Y-%m-%d") < datetime.strptime(curr_date, "%Y-%m-%d"):
                get_jobs_helper(job.daily_rate, job._hours, job)

            # if job date is equal to current working date and is_shift_over equals True
            # it means that the users shift is currently finished.
            elif datetime.strptime(job.date, "%Y-%m-%d") == \
                 datetime.strptime(curr_date, "%Y-%m-%d") and is_shift_over(job):
                 get_jobs_helper(job.daily_rate, job._hours, job)  


        elif active_jobs and datetime.strptime(job.date, "%Y-%m-%d") >= \
                             datetime.strptime(curr_date, "%Y-%m-%d") and\
                             not is_shift_over(job):
                get_jobs_helper(job.daily_rate, job._hours, job) # user has yet to work the shift

    return jobs, total_pay, total_hrs, worked_jobs
