#####################################################################
# Author = Egbie Uku
#####################################################################

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
