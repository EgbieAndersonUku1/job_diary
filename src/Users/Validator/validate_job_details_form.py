from flask import session
from src.Users.user import User
from datetime import datetime
from src.utilities.date_month_day_processor import month_to_num, check_date, translate_day
from src.utilities.job_processor import get_hours_worked
from src.utilities.time_processor import time_to_str
from src.models.Registrations.registration import Registration
import cgi

class ValidateJobDetailsForm(object):
    """Process the form and checks whether the details are correct"""
    def __init__(self, job_title, description, location,
                 rate, start_date, end_date, start_hours,
                 start_mins, end_hours, end_mins, day, is_shift_confirmed):

         self.errors = {}  # store all errors
         if start_date and end_date:
            # check whether the dates has the right format
            val, msg  = check_date(str(start_date))
            val_two, msg2 = check_date(str(end_date))
            if not val and not val_two:
                self.errors['date'] = msg
                self.errors['date'] = msg2
            elif val and not val_two:
                self.errors['date'] = 'end-date : {}'.format(msg2)
            elif not val and val_two:
                self.errors['date'] = 'start_date : {}'.format(msg)
            else:
               # checks whether the user's shift/job started on the day before
               # and finished on the next day.
               try:
                    start_time, finish_time = self.__concatenate_times(start_mins,
                                                                       start_hours,
                                                                       end_hours,
                                                                       end_mins)
                    time_to_str(get_hours_worked(start_date, start_time, end_date, finish_time))
               except UnboundLocalError:
                  self.errors['next_day'] = """It appears that your shift started the day
                                               before and ended the next day. In that case
                                               increment the end date day by one.
                                           """
               else:
                    self.start_mins, self.start_hours = start_mins, start_hours
                    self.end_mins, self.end_hours = end_mins, end_hours

         if not day or translate_day(day[:3]) == None:
             self.errors['day'] = 'The working day entered is incorrect'
         if not job_title:
             self.errors['job_title'] = 'The job title field must be not be empty'
         if not location:
             self.errors['job_loc'] = 'The job location field must be not be empty'
         if not description:
             self.errors['job_descr'] = 'The job description field must be not be empty'
         if not rate:
             self.errors['hourly_rate'] = 'The hourly rate field must be not be empty'
         if not start_date:
             self.errors['start_date'] = 'The start date field must be not be empty'
         if not end_date:
             self.errors['end_date'] = 'The end date field must be not be empty'

         # escape the html
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
         self.is_shift_confirmed = cgi.escape(is_shift_confirmed)
         self._job = None

    def verify_form(self):
        """Verify whether the form has any errors """
        self._job = ValidateJobDetailsForm(**self._get_json()) # set the obj to the ProcessForm
        if self.errors:
            return False, self.errors, self._job
        return True, self.errors, self._job

    def __concatenate_times(self, start_mins, start_hours, end_hours, end_mins):
    	"""Returns the start and finish time"""

        # guarantees that time is expessed as hh:mm
        if len(start_mins) == 1 and 1 <= int(start_mins) < 10:
    	       start_time  = start_hours + ':0' + start_mins
        if len(end_mins) == 1 and 1 <= int(end_mins) < 10:
    	      finish_time = end_hours   + ":0" + end_mins
        if len(start_mins) == 1 and not int(start_mins):
            start_time  = start_hours + ':00'
        if len(end_mins) == 1 and not int(end_mins):
    	      finish_time = end_hours   + ":00"
        if len(start_hours) == 2 and len(end_hours) == 2:
            start_time  = start_hours + ':' + start_mins # concatcenate the start hours and mins into hh:mm
            finish_time = end_hours   + ":" + end_mins
        else:
            start_time  = start_hours + ':' + start_mins # concatcenate the start hours and mins into hh:mm
            finish_time = end_hours   + ":" + end_mins   # concatcenate the end hours and mins into hh:mm
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
        start_time, finish_time = self.__concatenate_times(self.start_mins,
                                                           self.start_hours,
                                                           self.end_hours,
                                                           self.end_mins)
        if update:   # if update flag is set to true the row is updated.
            user = User(session['username'], start_date, end_date, day, _id=session['user_id'])
            record = user.add_job_to_records(self._job.job_title,
                                             self._job.description,
                                             self._job.location,
                                             start_time=start_time,
                                             finish_time=finish_time,
                                             hourly_rate=self._job.rate,
                                             is_shift_confirmed=self.is_shift_confirmed,
                                             update=True)
            return user.update_job(row_id, record) # update the row within the form

        user = User(session['username'], start_date, end_date, translate_day(day), _id=session['user_id']) # create a user object and add details to database
        return user.add_job_to_records(self._job.job_title,
                                       self._job.description,
                                       self._job.location,
                                       start_time=start_time,
                                       finish_time=finish_time,
                                       hourly_rate=self._job.rate,
                                       is_shift_confirmed=self.is_shift_confirmed,
                                       update=False)
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
            'day'         : self.day,
            'is_shift_confirmed': self.is_shift_confirmed}
