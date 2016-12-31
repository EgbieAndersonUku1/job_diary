#####################################################################
# Author = Egbie Uku
#####################################################################

from datetime import datetime
from dateutil import relativedelta
from src.utilities.common import create_flash_msg
import random

def _return_time_passed(start_date, start_time, finish_date, finish_time):
    """A wrapfunction that returned the years, month, hours, days, minutes
    passed between two dates.
    """
    year1, month1, day1 = start_date.split('-')
    year2, month2, day2 = finish_date.split('-')
    hours1, minutes1 = start_time.split(':')
    hours2, minutes2 = finish_time.split(':')
    first_date = datetime(int(year1), int(month1), int(day1), int(hours1), int(minutes1))
    sec_date   = datetime(int(year2), int(month2), int(day2), int(hours2), int(minutes2))
    return relativedelta.relativedelta(sec_date, first_date)

def _make_date_object(time, date):
    """takes a time in the form of (hh:mm) and date and creates a data
    object.
    """
    curr_time = datetime.now()
    hour = time.split(':')[0]
    mins = time.split(':')[1]
    year, month, day = date.split('-')

    date_obj = curr_time.replace(year=int(year),month=int(month),
                                 day=int(day), hour=int(hour),
                                 minute=int(mins))
    return curr_time, date_obj

def _check_shift(job, is_shift_now=False):
    """_check_shift(obj, str, str) -> returns(tuple)

       A wrapper function that returns the current time
       and the shift time date object.

       If the _is_shift_time is set to True returns:

         - The current time object and the the beginning
            of the shift start object.

       If the flag is set to False (default mode) returns the
       current date object and the end of the shift time
       date object.

       :parameters
           - job ; A job object.
           - is_shift_now : Default false. Used to calculate the
                            current date to the start of the
                            shift.
    """
    if is_shift_now:
        return _make_date_object(job.start_time, job.start_date)
    return _make_date_object(job.finish_time, job.end_date)

def is_shift_confirmed(job):
    """is_shift_confirmed(obj, func) -> returns(bool)

    Checks whether the user's shift/job is confirmed.

    :parameters
        - job: An object containg the user's job details.
        - returns: True if shift is confirmed and False otherwise.

    """
    return True if job.is_shift_confirmed.lower() == 'yes' else False

def is_shift_now(job):
    """is_shift_now(str) -> return(bool)

    Checks if the user shift has started. Returns True
    if it has or False if it has not.

    parameters:
       - job : An object that contains the job information.

    >>> is_shift_now(object(..))
    False
    >>> is_shift_now((object(..)))
    True
    """
    curr_time, shift_start_time = _check_shift(job, True)
    return True if curr_time >= shift_start_time else False

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
    curr_time, shift_end_time = _check_shift(job, False)
    return True if curr_time >= shift_end_time else False

def is_job_in_past_present_or_future(job, curr_date):
    """is_job_in_past_present_or_future(obj, str) -> return(str)

    Checks whether the job in question is either in the past,
    present or Future.
    """
    if datetime.strptime(job.start_date, "%Y-%m-%d") > datetime.strptime(curr_date, "%Y-%m-%d"):
        job = 'future'
    elif datetime.strptime(job.start_date, "%Y-%m-%d") == datetime.strptime(curr_date, "%Y-%m-%d"):
        job = 'present'
    else:
        job = 'past'
    return job

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
    return 'Starts in {}'.format(time_elasped) if time_elasped and int(time_elasped.split()[0]) > 0 else 'Job/shift in progress'

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

def get_jobs(active_jobs, permalink_jobs, jobs_obj, session, curr_date):
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
    user_jobs = jobs_obj(session['username'], _id=session['user_id'])
    total_pay, total_hrs, worked_jobs = [], [], []

    def get_jobs_helper(daily_rate, hrs, job):
        """returns the daily rate and the hours worked for the processed jobs"""
        total_pay.append(float(daily_rate))
        total_hrs.append(float(hrs))
        worked_jobs.append(job)

    if active_jobs:
        jobs = user_jobs.get_all_active_jobs() # sort job by ascending latest active job first
    elif permalink_jobs:
        jobs = permalink_jobs
    else:
        jobs = user_jobs.get_all_worked_jobs()  # sort job in descending order newest first
    for job in jobs:
        get_jobs_helper(job.daily_rate, job._hours, job) # user has yet to work the shift
    return total_pay, total_hrs, worked_jobs, user_jobs
