#####################################################################
# Author = Egbie Uku
#####################################################################

from datetime import datetime

def is_shift_now(start_hour, start_mins, end_hours, end_mins):
	curr_time = datetime.now()
	print start_hour, start_mins, end_hours, end_mins
	shift_start_time = curr_time.replace(hour=int(start_hour), minute=int(start_mins))
	shift_end_time = curr_time.replace(hour=int(end_hours), minute=int(end_mins))

	return True if shift_start_time <= curr_time <= shift_end_time else False



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
