###############################################################################
# Author : Egbie Uku
###############################################################################

from datetime import datetime

def mins_to_hours(minutes):
	"""mins_to_hours(float) -> return(str)

	Takes a time which is in either minutes or hours
	and converts to its string representation.

	:parameters
	   - minutes : either minutes/hrs and converts
	               to its string representation.
	               e.g 20.75 will be converted
	               to 21 hours and 25 minutes.

	>>> mins_to_hours(549)
	9 hours and 15 minutes
	"""
	try:
	      hrs, mins = str(minutes).split('.')
	except ValueError:
	     return time_to_str((minutes, 0))

	hour, minutes = str(minutes).split('.')
	if int(minutes) < 60:
		return time_to_str((hour, minutes))

	time = str(round((int(hour) + (int(minutes)/60.0)),2))
	hrs, mins = time.split('.')
	return time_to_str((hrs, int(mins)))

def time_to_units(time):
	"""time_to_units(tuple) -> returns(float)

	Takes a time tuple and returns the time as units.

	parameters:
		- time: tuple of two where the first elements is
		        hours and second is minutes.

	>>> time_to_unit((2,2))
	2.03
	>>> time_to_unit((10,15))
	10.25
	"""
	hours, minutes = time
	return hours +  round(minutes/60.0, 2)

def time_to_str(time):
	"""time_to_str(tuple) -> return(str)

	Takes a time tuple and returns the
	string representation of that tuple.

	parameters:
		- time: contains a tuple (h, m)
		        where the first element(h) is hours and
		        the second element(m) m is the minutes.

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

def month_to_str(month_num):
    '''month_to_str(str) -> return(str)

    Takes a number between 1-12 and returns a month name
    corresponding to that number. e.g 1-> January,
    2 -> Feb, etc.

    parameters:
       -month_num : Month in number e.g 1-12.

    >>> month_two_num(01)
    'January'
    '''
    months = {'1': 'January', '2':'February', '3':'March',
                  '4': 'April',   '5':'May',      '6': 'June',
                  '7':'July',     '8': 'August',  '9':'September',
              '10':'October', '11':'November','12': 'December'}
    return months.get(str(month_num), None)

def month_to_num(month):
    """month_to_num(str) -> return(str)

    Takes a month and if the first three characters
    match returns the month number corresponding to
    that month.

    e.g 1 -> January, 2 -> Feb, etc.

    parameters:
       -month : the month

    >>> month_two_num(January)
    '01'
    """
    months = {'Jan':'1', 'Feb':'2', 'Mar':'3',
                  'Apr':'4', 'May':'5', 'Jun':'6',
                  'Jul':'7', 'Aug':'8', 'Sep':'9',
              'Oct':'10','Nov':'11','Dec':'12'}
    return months.get(month.title(), None)