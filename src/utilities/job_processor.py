#####################################################################
# Author = Egbie Uku
#####################################################################

from datetime import datetime
from dateutil import relativedelta
import random

def is_shift_now(start_hour, start_mins, end_hours, end_mins):
    """is_shift_now(str, str, str, str) -> return(bool)

    Checks if the user shift has started. Returns True
    if it has or False if it has not.

    parameters:
       - start_hour : the hour part of the start time.
       - start_mins : The minute part of the hour time.
       - end_hours  : The hour part of the end time.
       - end_mins   : The minutes part of the end time

    >>> is_shift_now(11, 30, 00, 30)
    False
    >>> is_shift_now(11, 30, 21, 30)
    True
    """
    curr_time = datetime.now()
    shift_start_time = curr_time.replace(hour=int(start_hour), minute=int(start_mins))
    shift_end_time = curr_time.replace(hour=int(end_hours), minute=int(end_mins))
    return True if shift_start_time <= curr_time <= shift_end_time else False

def is_shift_over(end_hrs, end_mins):
    """is_shift_over(str, str) -> returns(bool)

    Use the current time and checks it against the user
    end shift time. Returns True if the shift is over 
    and False if is not.

    parameters:
       - end_hours  : The hour part of the end time.
       - end_mins   : The minutes part of the end time

    >>> is_shift_over(11, 30)
    False
    >>> is_shift_over(11, 21)
    True
    """
    curr_time = datetime.now()
    shift_end_time = curr_time.replace(hour=int(end_hrs), minute=int(end_mins))
    return True if curr_time > shift_end_time else False

def get_hours_worked(start_date, start_time, finish_date, finish_time):
    """get_hours_worked(str, str, str, str) -> return(tuple)

    Takes a starting date, starting time, ending date and a finishing time
    and returns the number of hours, minutes that has elasped between the
    two.

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
    year1, month1, day1 = start_date.split('-')  
    year2, month2, day2 = finish_date.split('-') 
    hours1, minutes1 = start_time.split(':')
    hours2, minutes2 = finish_time.split(':')
    first_date = datetime(int(year1), int(month1), int(day1), int(hours1), int(minutes1))
    sec_date   = datetime(int(year2), int(month2), int(day2), int(hours2), int(minutes2))
    difference = relativedelta.relativedelta(sec_date, first_date)

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
        - returns    : None if not found or an object if found
    """
    user = user_obj(session['username'], _id=session['user_id'])
    jobs, total_pay, total_hrs, worked_jobs =  user.get_by_user_id(), [], [], []

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
                           datetime.strptime(curr_date, "%Y-%m-%d") and \
                           is_shift_over(job.finish_time.split(':')[0],
                                         job.finish_time.split(':')[1]):
                          get_jobs_helper(job.daily_rate, job._hours, job)    
        elif active_jobs and datetime.strptime(job.date, "%Y-%m-%d") >= \
                          datetime.strptime(curr_date, "%Y-%m-%d") and \
                          not is_shift_over(job.finish_time.split(':')[0], 
                          job.finish_time.split(':')[1]):
                get_jobs_helper(job.daily_rate, job._hours, job) # user has yet to work the shift  
    return jobs, total_pay, total_hrs, worked_jobs
