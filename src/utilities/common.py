#####################################################################
# Author = Egbie Uku
#####################################################################

from flask import flash
from datetime import datetime
import random

def gen_row_id():
	"""_gen_row_id(void) -> return(str)
	A function that generates a five digit string. This will
	be used as a row id.
	"""
	return '#' + ''.join(['{}'.format(random.randint(1, 9)) for i in xrange(5)])

def get_questions():
	"""Returns a set of question. To be used in conjunction
	with forgotten password.
	"""
	QUESTION_ONE = "what is your mother's maiden name"
	QUESTION_TWO =  "what is your favourite activity"
	return QUESTION_ONE, QUESTION_TWO

def create_flash_msg(msg):
    """creates a message that will be output to screen"""
    flash(msg)

def get_curr_date():
	"""returns the current date along with the current day"""

	date = datetime.datetime.now()
	curr_day = datetime.date.today().strftime("%A")
	curr_date = "{}-{}-{}".format(date.year, date.month, date.day)
	return curr_day, curr_date
	
