#####################################################################
# Author = Egbie Uku
#####################################################################

import random
import bcrypt

def gen_row_id():
	"""_gen_row_id(void) -> return(str)
	A private function that generates a five digit string. This will
	be used as a row id.
	"""
	return '#' + ''.join(['{}'.format(random.randint(1, 9)) for i in xrange(5)])


def create_passwd_hash(password):
     """Takes a str and turns it into a hash"""
     return bcrypt.hashpw(password, bcrypt.gensalt(log_rounds=14))
   
def get_questions():
	"""
	"""
	QUESTION_ONE = 'Enter your login username'
	QUESTION_TWO = "what is your mother's maiden name"
	QUESTION_THREE = "where was your born"
	QUESTION_FOUR =  "who was your best friend at school"
	QUESTION_FIVE =  "what is your favourite activity"
	return QUESTION_ONE, QUESTION_TWO, QUESTION_THREE, QUESTION_FOUR, QUESTION_FIVE
	