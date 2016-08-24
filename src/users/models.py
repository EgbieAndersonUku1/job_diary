##################################################################
# Author : Egbie Uku
# The Login and Registration Model
##################################################################

from src.models.database import DataBase as db
import uuid
from datetime import datetime
import time
import bcrypt

class Login(object):
    """Login(class) -> Checks whether the user registration is valid.
    If not returns the appropriate response.
    """
    def __init__(self, username, password, is_logged_in=False, _id=None):
        self.login_id  = uuid.uuid4().hex if _id is None else _id
        self.username  = username
        self.password  = password
        self.is_logged_in   = is_logged_in
        self.logged_in_time = datetime.utcnow() # the time the user logged in

    def _get_user_login_details(self):
        """func : _get_user_login_details(None) -> return(obj or None)
        Helper function: Checks whether the user details returns obj or False
        otherwise.
        """
        login_data = db.find_one(collections='login_credentials', query={'username': self.username})
        if not login_data:
            return False
        del login_data['_id']
        return Login(**login_data) # return users logging details as an obj if found false otherwise

    def is_credentials_ok(self):
        """func : check_user_details(None) -> return(None)
        Checks whether the users details are correct. Returns True if it is
        and False otherwise
        """
        login_obj = self._get_user_login_details()
        if not login_obj:
            return False  # users details does not exist

        # users details found verify login in details
        if bcrypt.hashpw(self.password, login_obj.password) == login_obj.password:
            self.is_logged_in = True # set the login to true
            return True              # users details check out
        return False                 # users details did not check out

    def save(self):
        db.insert(collection='login_credentials', data=self._json())

    def _json(self):
        return {'username'    : self.username,
                'password'    : self.password,
                'is_logged_in': self.is_logged_in,
                'login_id'    : self.login_id}

class Registration(object):
    """Registration(class)
    Allows the user to register their details.
    """
    def __init__(self, full_name, email, password, registration_date=None, _id=None):
        self.full_name = full_name
        self.email     = email
        self.password  = password
        self.registration_id = uuid.uuid4().hex if _id is None else _id
        self.registration_date = registration_date

    def _is_user_name_unique(self, email):
        """check whether the username is unique"""

        if db.find_one(collections='login_credentials', query={'email': self.email}):
            return False # False means the users with that email already exists
        return True

    def register(self):
        """register the user"""

        if not self._is_user_name_unique(self.email):
            return False

        # Takes the users name, email and the hashed password and stores in database
        salt = bcrypt.gensalt(log_rounds=18)
        hash_password = bcrypt.hashpw(self.password, salt)
        self.password = hash_password
        self._save()
        return True # True Means that everything was created smoothly

    def _save(self):
        """Saves the registration details to the database"""
        db.insert(collection='user_credentials', data=self._get_json())

    def _get_json(self):
        """Get the details of the registration in the form of a json format """
        return {'full_name'     : self.full_name,
                'email'         : self.email,
                'password'      : self.password,
                'registration_date': time.strftime("%d/%m/%Y"),
                'registration_id'  : self.registration_id
                }
