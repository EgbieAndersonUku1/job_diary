##################################################################
# Author : Egbie Uku
# The Login and Registration Model
##################################################################

from src.models.database import DataBase as db
from src.models.utils import translate_day
from src.models.utils import get_hours_worked, time_to_str, translate_day
from flask import session
from src.models.users import User
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
    def __init__(self, username, password, _id=None,
                 is_admin=False, logged_in_time=datetime.utcnow()):

        self.username  = username
        self.password  = password
        self._id  = uuid.uuid4().hex if _id is None else _id
        self.is_admin  = is_admin
        self.logged_in_time = logged_in_time                  # the time the user logged in

    def _get_user_login_details(self):
        """func : _get_user_login_details(None) -> return(obj or None)
        Helper function: Checks whether the user details returns obj or False
        otherwise.
        """
        login_data = db.find_one(collections='login_credentials', query={'username': self.username})
        return False if not login_data else Login(**login_data)

    def is_credentials_ok(self):
        """func : check_user_details(None) -> return(None)
        Checks whether the users details are correct. Returns True if it is
        and False otherwise
        """
        login_obj = self._get_user_login_details()
        if not login_obj:
            return False # users details does not exist
        return (login_obj if bcrypt.hashpw(self.password, login_obj.password) == login_obj.password else False) # users details found verify login in details

    def de_activate_login(self):
        pass

    def save(self):
        """Saves the form to the database in json format"""
        db.insert_one(collection='login_credentials', data=self._json())

    def _json(self):
        """returns a json representation of the form"""
        return {'username'      : self.username,
                'password'      : self.password,
                'is_admin'      : self.is_admin,
                '_id'           : self._id,
                'logged_in_time': self.logged_in_time }

class Registration(object):
    """Registration(class)
    Allows the user to register their details.
    """
    def __init__(self, email, password, registration_date=None, _id=None):
        self.email      = email
        self.password   = password
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
        self._save()  # save the encrypted password and username to database
        return True # True Means that everything was created smoothly

    def _save(self):
        """Saves the registration details to the database in json format"""
        db.insert_one(collection='user_credentials', data=self._get_json())

    def _get_json(self):
        """Get the details of the registration in the form of a json format """
        return {'email'            : self.email,
                'password'         : self.password,
                'registration_date': time.strftime("%d/%m/%Y"),
                'registration_id'  : self.registration_id }

class ProcessForm(object):
    """Process the form and checks whether the details are correct"""
    def __init__(self, job_title, description, location,
                 rate, start_date, end_date, start_hours,
                 start_mins, end_hours, end_mins, day):

         self.errors = {} # pass to the user so they can see there errors
         # check whether the dates are in the format dd/mm/yyyy
         if start_date and end_date:
             st_date = start_date.split('/')
             en_date = end_date.split('/')
             if len(st_date) and len(en_date) == 3: # check whether dates are numbers
                 if not(str(st_date[0]).isdigit() and str(st_date[1]).isdigit() and str(st_date[2]).isdigit()):
                     self.errors['start_date'] = 'The start date has an incorrect format. Format(dd/mm/yyyy)'
                 if not(str(en_date[0]).isdigit() and str(en_date[1]).isdigit() and str(en_date[2]).isdigit()):
                     self.errors['end_date'] = 'The end date has an incorrect format. Format (dd/mm/yyyy)'
             else:
                self.errors['date'] = 'One or more of dates has an incorrect format'

         if (start_hours == end_hours and start_mins == end_mins) and (datetime.strptime(str(end_date), "%d/%m/%Y") == datetime.strptime(str(start_date), "%d/%m/%Y")):
            self.errors['time'] = 'The  start and end time cannot be the same if start date and end dates equal'
         if not day or translate_day(day[:3]) == None:
             self.errors['day'] = 'The working day entered is incorrect'
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
         if datetime.strptime(str(end_date), "%d/%m/%Y") < datetime.strptime(str(start_date), "%d/%m/%Y"):
              self.errors['days_error'] = 'The end date cannot be less then the start date'
         #if int(start_hours) != '0' and int(end_hours) >= 0 and  datetime.strptime(str(end_date), "%d/%m/%Y") == datetime.strptime(str(start_date), "%d/%m/%Y"):
         #  self.errors['day_change'] = 'The start & end times you entered shows that you finished the next day increment the end date by one'

        #if start date and end date is True check whether there are in the form of dd/mm/yyyy
         self.job_title   = cgi.escape(job_title).title()
         self.description = cgi.escape(description).title()
         self.location    = cgi.escape(location).title()
         self.rate = cgi.escape(rate)
         self.start_date = cgi.escape(start_date).title()
         self.end_date   = cgi.escape(end_date).title()
         self.start_hours = cgi.escape(start_hours).title()
         self.start_mins  = cgi.escape(start_mins).title()
         self.end_hours   = cgi.escape(end_hours).title()
         self.end_mins = cgi.escape(end_mins).title()
         self.day      = cgi.escape(day)
         self._obj = None

    def verify_form(self):
        """Verify whether the form has any errors """
        self._obj = ProcessForm(**self._get_json()) # set the obj to the ProcessForm
        if self.errors:
            return False, self.errors, self._obj
        return True, self.errors, self._obj

    def _concatcenate_time_str(self):
    	""" Takes two strings and concatcenates them together creating a time string"""

        # guarantees that time is expressed as hh:mm
        if len(self._obj.start_mins) == 1 and 1 <= int(self._obj.start_mins) < 10:
    	       start_time  = self._obj.start_hours + ':0' + self._obj.start_mins
        if len(self._obj.end_mins) == 1 and 1 <= int(self._obj.end_mins) < 10:
    	      finish_time = self._obj.end_hours   + ":0" + self._obj.end_mins
        if len(self._obj.start_mins) == 1 and not int(self._obj.start_mins):
            start_time  = self._obj.start_hours + ':00'
        if len(self._obj.end_mins) == 1 and not int(self._obj.end_mins):
    	      finish_time = self._obj.end_hours   + ":00"
        if len(self._obj.start_hours) == 2 and len(self._obj.end_hours) == 2:
            start_time  = self._obj.start_hours + ':' + self._obj.start_mins # concatcenate the start hours and mins into hh:mm
            finish_time = self._obj.end_hours   + ":" + self._obj.end_mins 

        else:
            start_time  = self._obj.start_hours + ':' + self._obj.start_mins # concatcenate the start hours and mins into hh:mm
            finish_time = self._obj.end_hours   + ":" + self._obj.end_mins   # concatcenate the end hours and mins into hh:mm

    	return start_time, finish_time

    def process_form(self, start_date, end_date, day):
        """process_form(str, str, str) -> return(str)

        params start_date: A start date string
        params end_date  : The end date string
        params day       : The day string
        params return    : returns a row id in the form a string

        Process the form and adds the user details to the database.
        """
        # to be use with pymongo sorting for the database. Pymongo seems to have
        # trouble sorting dates if 0 is not in front of a single digits. For example
        # when sorting in smallest first it would place 19/09/2016 before 9/09/2016

        start_time, finish_time = self._concatcenate_time_str()
        hours = get_hours_worked(start_date, start_time, end_date, finish_time)
        user = User(session['username'], start_date, end_date, translate_day(day), _id=session['user_id']) # create a user object and add details to database
        return (user.add_job_details(self._obj.job_title, self._obj.description,
                                     self._obj.location, start_time, finish_time,
                                     self._obj.rate))
    def _get_json(self):
        """Returns the details of the form in json"""
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
