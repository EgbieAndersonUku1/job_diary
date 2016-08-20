
def translate_month(month):
	'''translate_month(str) -> return(str)
	Takes a string digit and returns the month equivalent of that
	string.

	>>> translate_month(01)
	'January'
	'''
	months = {'01': 'January', '02':'February', '03':'March',
		      '04': 'April',   '05':'May',      '06': 'June',
		      '07':'July',     '08': 'August',  '09':'September',
	          '10':'October',  '11':'November', '12': 'December'}
	return months[month]

def translate_to_month_num(month_num):
	"""translate_to_month_num(int) -> return(str)
	Takes a number between 1-12 and returns a month name
	corresponding to that number.

	e.g 1 returns January, 2 returns Feb, etc

	>>> translate_to_month_num(01)
	'January'
	"""
	months = {'January':'01', 'February':'02', 'March':'03',
		      'April':'04',   'May':'05', 'June':'06',
		      'July':'07', 'August':'08',  'September':'09',
	          'October':'10',  'November':'11', 'December':'12'}
	return months[month.title()]
