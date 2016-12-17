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

def create_passwd_hash(passwd):
    """create_passwd_hash(str)
    Hashes a password for the first time

    >>>create_passwd_hash(password)
    hashed password
    """
    return bcrypt.hashpw(passwd, bcrypt.gensalt(log_rounds=14))

def check_passwd_hash(passwd, hashed_passwd):
 	"""Check that a unhashed password matches one that has previously been hashed

 	:parameters
 	    - passwd : The unhashed password.
 	    - hashed_passwd: The hashed password.
 	"""
 	return bcrypt.hashpw(passwd, hashed_passwd) == hashed_passwd
   
def get_questions():
	"""
	"""
	QUESTION_ONE = "what is your mother's maiden name"
	QUESTION_TWO =  "what is your favourite activity"
	return QUESTION_ONE, QUESTION_TWO
	