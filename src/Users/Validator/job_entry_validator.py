from flask import session
from datetime import datetime
from src.Users.Validator.date_validator import check_date, check_day
from src.utilities.converter import month_to_num, time_to_str
from src.Users.Jobs.job_helper import get_hours_worked
from src.Users.Models.Registrations.registration import Registration
from cgi import escape

class ValidateJobDetailsForm(object):
    """Process the form and checks whether the job details entered by the user are correct"""
    def __init__(self, job_title, description, location,
                 rate, start_date, end_date, day, is_shift_confirmed,
                 start_hours, start_mins, end_hours, end_mins,
                 worked_job='No'):

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
                    self.start_time = self.__join_hour_and_minute(start_hours, start_mins)
                    self.finish_time = self.__join_hour_and_minute(end_hours, end_mins)
                    time_to_str(get_hours_worked(start_date, self.start_time, end_date, self.finish_time))
               except UnboundLocalError, ValueError:
                  self.errors['next_day'] = """It appears that your shift started
                                               the day before and ended the next
                                               day. In that case increment the
                                               end date day by one.
                                             """
               else:
                    # split the hh:mm and store in their respective names.
                    self.start_hours, self.start_mins = self.start_time.split(':')
                    self.end_hours, self.end_mins = self.finish_time.split(':')

         if not day or check_day(day[:3]) == None:
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
         self.job_title   = escape(job_title, quote=True).title()
         self.description = escape(description, quote=True).title()
         self.location    = escape(location, quote=True).title()
         self.rate = escape(rate, quote=True)
         self.start_date = escape(start_date, quote=True).title()
         self.end_date   = escape(end_date, quote=True).title()
         self.start_hours = escape(start_hours, quote=True).title()
         self.start_mins  = escape(start_mins, quote=True).title()
         self.end_hours   = escape(end_hours, quote=True).title()
         self.end_mins = escape(end_mins, quote=True).title()
         self.day      = escape(day, quote=True)
         self.is_shift_confirmed = escape(is_shift_confirmed)
         self._job = None
         self.worked_job = worked_job

    def __join_hour_and_minute(self, hour, minute):
    	"""__join_hour_and_minute(str, str) -> return(str)

        A private function that takes two parameters the hour (hh),
        part of the time and  minute (mm) part of the time.
        And then concatcenates the hour part with the minute.
        The final result is a single string in the form hh:mm.

        :parameters
            - hour: The hour part of the time.
            - minute : The minutes part the time.

        >>> hour, minute = 19, 43
        >>> __join_hour_and_minute(hour, minute)
        >>> 19:43
        >>> hour, minute = 1, 3
        >>> __join_hour_and_minute(hour, minute)
        >>> 01:03
        """
        # guarantees that time is expessed as hh:mm
        if len(str(hour)) == 1:
            hour = '0{}'.format(hour)
        if len(str(minute)) == 1:
            minute = '0{}'.format(minute)
        return '{}:{}'.format(hour, minute)

    def _get_json(self):
        """Returns the jobs attributes in json format"""
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

    def verify_form(self):
        """verify_form(None) -> return(tuple)

        Verify whether the form itself has any errors.
        Returns a tuple of three elements. The first element
        is a boolean value True if the form has no errors and False
        otherwise. The second element is a dictionary containing
        all errors found, an empty dictionary if no errors are found.
        details e.g title, description, etc. Finally the third element
        is the job object containing the user's
        """
        self._job = ValidateJobDetailsForm(**self._get_json()) # set the obj to the ProcessForm
        if self.errors:
            return False, self.errors, self._job
        return True, self.errors, self._job
