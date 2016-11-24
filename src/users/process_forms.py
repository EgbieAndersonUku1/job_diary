from flask import session
from src.models.users import User
from datetime import datetime
from src.utilities.date_month_day_processor import month_to_num, check_date, translate_day
from src.utilities.job_processor import get_hours_worked
import cgi

class ProcessForm(object):
    """Process the form and checks whether the details are correct"""
    def __init__(self, job_title, description, location,
                 rate, start_date, end_date, start_hours,
                 start_mins, end_hours, end_mins, day):

         self.errors = {}  # pass to the user so they can see there errors

         if start_date and end_date:
            # check whether the dates has the right format
            val, msg  = check_date(str(start_date)) 
            val_two, msg2 = check_date(str(end_date))
            if not val and not val_two:
                self.errors['date'] = msg
                self.errors['date'] = msg2
            elif val and not val_two:
                self.errors['date'] = 'end-date has {}'.format(msg2)
            elif not val and val_two:
                self.errors['date'] = 'start_date has {}'.format(msg)
            else:
                if (start_hours == end_hours and start_mins == end_mins) and (datetime.strptime(str(end_date), "%Y-%m-%d") == datetime.strptime(str(start_date), "%Y-%m-%d" )):
                    self.errors['time'] = 'The  start and end time cannot be the same if start date and end dates equal'
                if datetime.strptime(str(end_date), "%Y-%m-%d") < datetime.strptime(str(start_date), "%Y-%m-%d"):
                    self.errors['days_error'] = 'The end date cannot be less then the start date'
                      
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

    def get_start_and_finish_time(self):
    	"""Returns the start and finish time"""

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

    def process_form(self, start_date, end_date, day, row_id=None, update=False):
        """process_form(str, str, str, optional str, optional bool) -> return(str)

        @params 
        start_date: A start date string
        end_date  : The end date string
        day       : The day string
        returns   : returns a row id if update flag is on and None if update flag is off

        optional flags
        -------------
        row_id: The row id which corresponds to a row in database
        update: When update is True the row will be updated with new data
       
        Process the form and adds the user details to the database.
        """
        start_time, finish_time = self.get_start_and_finish_time()
        if update:   # if update flag is set to true the row is updated.
            user = User(session['username'], start_date, end_date, day, _id=session['user_id'])
            form_obj = user.add_job_details(self._obj.job_title, 
                                            self._obj.description,
                                            self._obj.location, 
                                            start_time, 
                                            finish_time, 
                                            self._obj.rate, update=True)
            return user.update_row(row_id, form_obj) # update the row within the form

        user = User(session['username'], start_date, end_date, translate_day(day), _id=session['user_id']) # create a user object and add details to database
        return user.add_job_details( self._obj.job_title, 
                                     self._obj.description,
                                     self._obj.location, 
                                     start_time, 
                                     finish_time,
                                     self._obj.rate)
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

class ProcessSearchForm(object):
    """ProcessSearchForm(class)
    Checks and process the search form template.
    """
    def __init__(self, form):
        self.job_title = form.job_title.data
        self.location  = form.location.data
        self.hrs_worked = form.hrs_worked.data
        self.year = form.year.data
        self.month     = form.month.data
        self.date = form.date.data
        self.day  = form.day.data
        self.start_time = form.start_time.data
        self.finish_time = form.finish_time.data
        self.daily_rate  = form.daily_rate.data
        self.val_one = form.month_one.data
        self.val_two = form.month_two.data
        self._user = user = User(session['username'], _id=session['user_id'])
        self.days = {'Mon': 'Monday', 'Tue': 'Tuesday', 'Wed': 'Wednesday',
                     'Thu':'Thursday', 'Fri': 'Friday', 'Sat': 'Saturday',
                     'Sun': 'Sunday'}

    def _fix_time_str(self, time):
        # Temporay solution until I fix it: Databases stores values that end in 00 as 0
        # due to one of my modules e.g 17:00 is stored as 17:0
        return (time[:-1]  if len(time) == 5 and time[3] == '0' else time)

    def _is_date_str(self, date):
        """Returns True if date is in word format or False if date is in YYYY-MM-DD"""
        return date.isalpha()

    def process_dates(self, val, val2):
        """turn the dates into their month representives"""
        if self._is_date_str(val) and self._is_date_str(val2):
            if month_to_num(val[:3].title()) and month_to_num(val2[:3].title()):
                return self._user.get_by_month_range(val, val2)
        elif not self._is_date_str(val) and not self._is_date_str(val2):
            return self._user.get_by_date_range(val, val2)

    def get_data(self):
        """retreive and process the data from the search form template"""
        if self.job_title:
            return self._user.get_by_job_title(self.job_title.title())
        elif self.location:
            return self._user.get_by_location(self.location)
        elif self.date:
            return self._user.get_by_date(str(self.date))
        elif self.day:
            return self._user.get_by_day(self.days.get(self.day.title()[:3], None))
        elif self.start_time:
            return self._user.get_by_start_time(self._fix_time_str(str(self.start_time)))
        elif self.finish_time:
            return self._user.get_by_finish_time(self._fix_time_str(str(self.finish_time)))
        elif self.hrs_worked:
            return self._user.get_by_hours(self.hrs_worked)
        elif self.month:
            return self._user.get_by_month(str(self.month[0:3].title()))
        elif self.daily_rate:
            return self._user.get_by_daily_rate(self.daily_rate)
        elif self.val_one and self.val_two:
            return self.process_dates(self.val_one, self.val_two)
        elif self.year:
            return self._user.get_by_year(self.year)
        