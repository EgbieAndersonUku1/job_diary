#####################################################################
# Author = Egbie Uku
#####################################################################

import bcrypt

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
