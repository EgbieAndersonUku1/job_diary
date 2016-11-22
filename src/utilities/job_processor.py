#####################################################################
# Author = Egbie Uku
#####################################################################


from datetime import datetime
from dateutil import relativedelta
import random

def get_hours_worked(start_date, start_time, finish_date, finish_time):
	"""get_hours_worked(str, str, str, str) -> return(tuple)

	@params    :
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

def get_daily_rate(units, hourly_rate):
	"""get_daily_rate(float, float) -> returns(float)

	@params   
	units         : The time in units
	hourly_rate   : The amount paid in hours
	returns       : The total amount paid for the day
	"""
	return round((units * float(hourly_rate)), 2)

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