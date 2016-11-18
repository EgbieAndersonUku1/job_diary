########################################################################
# Author : Egbie Uku
#########################################################################

from datetime import datetime
from dateutil import relativedelta
import random

def check_date(date):
    """check_date(str) -> return(True or str)
    Takes a date and checks if the date is in the format
    of YYYY-MM-DD.

    Returns True if date is in the right format and returns
    error message if the date is not.
    """
    if date != None:
        if len(date) == 10 :
            if '-' in date:
                    year, month, day = date.split('-')
                    if year.isdigit() and len(year) == 4:
                            if month.isdigit() and len(month) == 2:
                                    if day.isdigit() and len(day) == 2:
                                            return True
                                    return 'day must be in the format of DD'
                            return 'month must be in the format of MM'
                    return 'year must be YYYY'
            return 'add "-" in between YYYY-MM-DD'
        return 'incorrect date format try YYYY-MM-DD'
    return 'date cannot be None'


def translate_day(day):

	days = {'mon': 'Monday',    'tue' : 'Tuesday',
	       'wed' : 'Wednesday', 'thu' : 'Thursday',
		   'fri' : 'Friday',    'sat' : 'Saturday',  'sun' : 'Sunday'}
	return days.get(str(day[0:3]).lower())

def month_to_str(month_num):
	'''month_to_str(str) -> return(str)
	Takes a string digit and returns the month equivalent of that
	string.
	>>> month_to_str(1)
	'January'
	'''
	months = {'1': 'January', '2':'February', '3':'March',
		      '4': 'April',   '5':'May',      '6': 'June',
		      '7':'July',     '8': 'August',  '9':'September',
	          '10':'October', '11':'November','12': 'December'}
	return months.get(str(month_num), None)

def month_to_num(month):
	"""month_to_num(int) -> return(str)
	Takes a number between 1-12 and returns a month name
	corresponding to that number.

	e.g 1 returns January, 2 returns Feb, etc

	>>> month_two_num(01)
	'January'
	"""
	months = {'Jan':'1', 'Feb':'2', 'Mar':'3',
		      'Apr':'4', 'May':'5', 'Jun':'6',
		      'Jul':'7', 'Aug':'8', 'Sep':'9',
	          'Oct':'10','Nov':'11','Dec':'12'}
	return months.get(month.title(), None)

def get_hours_worked(start_date, start_time, finish_date, finish_time):
	"""get_hours_worked(str, str, str, str) -> return(tuple)

	start_date : The beginning date in the form of dd/mm/yy
	end_date   : The ending date in the form of dd/mm/yy
	start_time : The starting time in the form of hh:mm
	finish_time: The starting time in the form of hh:mm
	returns    : A tuple where the first element is the hours and second the minutes

	Takes a starting date, starting time, ending date and a finishing time
	and returns the number of hours, minutes that has elasped between the
	two

	>>> get_hours_worked('1/1/2016', '1/1/2016', '9:23', '21:26')
	(12, 3)
	>>> get_hours_worked('1/1/2016', '1/4/2016', '9:23', '21:26')
	(83, 43)
	"""
	year1, month1, day1 = start_date.split('-')  # split the dates for the start date by  /
	year2, month2, day2 = finish_date.split('-') # split the dates for the finish date by /
	hours1, minutes1 = start_time.split(':')
	hours2, minutes2 = finish_time.split(':')
	first_date = datetime(int(year1), int(month1), int(day1), int(hours1), int(minutes1))
	sec_date   = datetime(int(year2), int(month2), int(day2), int(hours2), int(minutes2))
	difference = relativedelta.relativedelta(sec_date, first_date)

	# if start date is not equal to the finish date it means that user
	# started on one day and finish on another day
	if start_date != finish_date:
		hours = difference.days * 24           # convert days to hours
		total_hours = difference.hours + hours # add the converted days hours to number of time hours worked
		return total_hours, difference.minutes
	return difference.hours, difference.minutes

def gen_row_id():
	"""_gen_row_id(void) -> return(str)
	A private function that generates a five digit string. This will
	be used as a row id.
	"""
	return '#' + ''.join(['{}'.format(random.randint(1, 9)) for i in xrange(5)])

def get_daily_rate(units, hourly_rate):
	"""get_daily_rate(tuple, float or int) -> returns(float)
	hours         : (h, m)
	hourly_rate   : The amount paid in hours
	returns float : The total amount paid for the day
	"""
	return units * float(hourly_rate)

def time_to_units(time):
	"""time_to_units(tuple) -> returns(float)

	@params:
	time   : tuple of two where the first elements is hours and second is minutes
	returns: returns time in units

	>>> time_to_unit((2,2))
	2.03
	>>> time_to_unit((10,15))
	10.25
	"""
	hours, minutes = time
	return hours +  round(minutes/60.0, 2)

def time_to_str(time):
	"""time_to_str(tuple) -> return(str)

	time   : contains a tuple (h, m) where is the hours and m is the minutes
	return : return the time in string format

	>>> time_to_str((1, 0))
	1 hour
	>>> time_to_str((2, 0))
	2 hours
	>>> time_to_str((0, 1))
	1 minute
	>>> time_to_str((0, 10))
	10 minutes
	"""
	hours, mins = time

	if hours > 1 and mins >1:
		time_str = '{} hours and {} minutes'.format(hours, mins)
	elif hours==1 and mins == 1:
		time_str = '{} hour and {} minute'.format(hours, mins)
	elif hours==1 and mins > 1:
		time_str = '{} hour and {} minutes'.format(hours, mins)
	elif hours>1 and mins ==1:
		time_str = '{} hours  and {} minute'.format(hours, mins)
	elif not hours and mins > 1:
		time_str = '{} minutes '.format(mins)
	elif not hours and mins == 1:
		time_str = '{} minute'.format(mins)
	elif hours == 1 and not mins:
		time_str = '{} hour'.format(hours)
	elif hours > 1 and not mins:
		time_str = '{} hours '.format(hours)
	return time_str

def get_jobs(active_jobs, user_obj, session, curr_date):
    """get_job sorts the active jobs from the none active jobs

    @params: 
    active_jobs: flag that tells the function to only search for active jobs
    user_obj   : user object module
    session    : The session belonging to the user 
    curr_date  : The current date
    returns    : None if not found or an object if found
    """
    user = user_obj(session['username'], _id=session['user_id'])
    jobs, total_pay, total_hrs, worked_jobs =  user.get_by_user_id(), [], [], []

    def get_jobs_helper(daily_rate, hrs, job):
        """returns the daily rate and the hours worked for the processed jobs"""
        total_pay.append(float(job.daily_rate))
        total_hrs.append(float(job._hours))
        worked_jobs.append(job)

    for job in jobs:
        if not active_jobs:
            if datetime.strptime(job.date, "%Y-%m-%d") < datetime.strptime(curr_date, "%Y-%m-%d"):
                get_jobs_helper(job.daily_rate, job._hours, job)
        elif active_jobs and datetime.strptime(job.date, "%Y-%m-%d") >= datetime.strptime(curr_date, "%Y-%m-%d"):
                get_jobs_helper(job.daily_rate, job._hours, job)
    return jobs, total_pay, total_hrs, worked_jobs
