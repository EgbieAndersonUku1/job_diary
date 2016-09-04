##################################################################
# Author : Egbie Uku
# The Login and Registration Model
##################################################################

from src.models.database import DataBase as db
from src.models.utils import translate_day
import cgi
from flask import request
import uuid
from datetime import datetime
import time
import bcrypt


class Login(object):
    """Login(class) -> Checks whether the user registration is valid.
    If not returns the appropriate response.
    """
    def __init__(self, username, password, is_logged_in=False, _id=None,
                users_deactivate_login=False, admin_deactivate_login=False,
                logged_in_time=datetime.utcnow()):

        self._id  = uuid.uuid4().hex if _id is None else _id
        self.username  = username
        self.password  = password
        self.is_logged_in   = is_logged_in
        self.logged_in_time = logged_in_time                  # the time the user logged in
        self.users_deactivate_login  = users_deactivate_login # User can de_activate user login
        self.admin_deactivate_login  = admin_deactivate_login # Admin can de_activate their own account

    def _get_user_login_details(self):
        """func : _get_user_login_details(None) -> return(obj or None)
        Helper function: Checks whether the user details returns obj or False
        otherwise.
        """
        login_data = db.find_one(collections='login_credentials', query={'username': self.username})
        if not login_data:
            return False
        #del login_data['_id']
        return Login(**login_data) # return users logging details as an obj if found false otherwise

    def is_credentials_ok(self):
        """func : check_user_details(None) -> return(None)
        Checks whether the users details are correct. Returns True if it is
        and False otherwise
        """
        login_obj = self._get_user_login_details()
        if not login_obj:
            return False  # users details does not exist

        # check if the account has been disable by ADMIN
        if login_obj.admin_deactivate_login:
            msg = 'Your account has been de-activate by admin. Contact admin to re-activate'
            return False, msg

        # users details found verify login in details
        elif bcrypt.hashpw(self.password, login_obj.password) == login_obj.password:
            self.is_logged_in = True # set the login to true
            return True              # users details check out
        return False                 # users details did not check out

    def de_activate_login(self):
        pass

    def save(self):
        db.insert_one(collection='login_credentials', data=self._json())

    def _json(self):
        return {'username'              : self.username,
                'password'              : self.password,
                'is_logged_in'          : self.is_logged_in,
                '_id'                   : self._id,
                'logged_in_time'        : self.logged_in_time,
                'users_deactivate_login': self.users_deactivate_login,
                'admin_deactivate_login': self.admin_deactivate_login }

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
        # False means that the user was found, True means that no user was found by that name
        return False if db.find_one(collections='login_credentials', query={'username': self.email}) else True

    def register(self):
        """register the user"""

        if not self._is_user_name_unique(self.email):
            return False

        # Takes the users name, email and the hashed password and stores in database
        salt = bcrypt.gensalt(log_rounds=14)
        hash_password = bcrypt.hashpw(self.password, salt)
        self.password = hash_password
        self._save()
        return True # True Means that everything was created smoothly

    def _save(self):
        """Saves the registration details to the database"""
        db.insert_one(collection='user_credentials', data=self._get_json())

    def _get_json(self):
        """Get the details of the registration in the form of a json format """
        return {'full_name'        : self.full_name,
                'email'            : self.email,
                'password'         : self.password,
                'registration_date': time.strftime("%d/%m/%Y"),
                'registration_id'  : self.registration_id
                }


class ProcessForm(object):

    def __init__(self, job_title, description, location,
                 rate, start_date, end_date, start_hours,
                 start_mins, end_hours, end_mins, day):

         self.errors = {}
         if not day or translate_day(day) == None:
             self.errors['day'] = 'Enter the correct working day or leave blank for current day'
         if not job_title:
             self.errors['job_title'] = 'The job title field must be not be empty'
         if not location:
             self.errors['job_loc']   = 'The job location field must be not be empty'
         if not description:
             self.errors['job_descr'] = 'The job description field must be not be empty'
         if not rate:
             self.errors['hourly_rate'] = 'The hourly rate field must be not be empty'
         if not start_date:
             self.errors['start_date']  = 'The start date field must be not be empty'
         if not end_date:
             self.errors['end_date']   = 'The end date field must be not be empty'
         if end_date < start_date:
             self.errors['days_error'] = 'The end date cannot be less then the start date'
         if start_hours == end_hours:
             self.errors['start_hours'] = 'The start time and the end time cannot be the same'

         self.job_title  = cgi.escape(job_title).title()
         self.description = cgi.escape(description).title()
         self.location    = cgi.escape(location).title()
         self.rate = cgi.escape(rate)
         self.start_date = cgi.escape(start_date).title()
         self.end_date   = cgi.escape(end_date).title()
         self.start_hours = cgi.escape(start_hours).title()
         self.start_mins = cgi.escape(start_mins).title()
         self.end_hours = cgi.escape(end_hours).title()
         self.end_mins = cgi.escape(end_mins).title()
         self.day     = cgi.escape(day)


    def verify_form(self):
        if self.errors:
            return False, self.errors, ProcessForm(**self._get_json())
        return True, self.errors, ProcessForm(**self._get_json())

    def _get_json(self):
        return {
            'job_title'   : self.job_title,
            'location'    : self.location,
            'description' : self.description,
            'rate'        : self.rate,
            'start_date'  : self.start_date,
            'end_date'    : self.end_date,
            'start_hours' : self.start_hours,
            'start_mins'  : self.start_mins,
            'end_hours'   : self.end_hours,
            'end_mins'    : self.end_mins,
            'day'         : self.day
            }
