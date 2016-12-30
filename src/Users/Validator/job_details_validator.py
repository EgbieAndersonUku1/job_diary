from flask import session
from src.Users.user import User
from datetime import datetime
from src.Users.Validator.date_validator import check_date, check_day
from src.utilities.converter import month_to_num, time_to_str
from src.Users.Jobs.job_helper import get_hours_worked
from src.Users.Models.Registrations.registration import Registration
from cgi import escape
from src.utilities.common import create_flash_msg
from src.Users.Jobs.job_helper import (is_shift_over,
                                       has_previous_job_been_worked,
                                       is_job_in_past_present_or_future,
                                       is_shift_confirmed,
                                       is_shift_now)

class ValidateJobDetailsForm(object):
    """Process the form and checks whether the job details entered by the user are correct"""
    def __init__(self, job_title, description, location,
                 rate, start_date, end_date, day, is_shift_confirmed,
                 start_hours='00', start_mins='00', end_hours='00', end_mins='00'):

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

    def __save(self, user, row_id=None, update=False):
        """The save function saves the data to database. If row_id is not
        false and update is equal to true updates a previous row with the
        new data.

        Returns a row id.
        """
        return user.add_job_to_records(self._job.job_title,
                                       self._job.description,
                                       self._job.location,
                                       start_time=self.start_time,
                                       finish_time=self.finish_time,
                                       hourly_rate=self._job.rate,
                                       is_shift_confirmed=self.is_shift_confirmed,
                                       update=update, row_id=row_id)

    def __update_job_status(self, user, status):

        row_id = self.__save(user)
        user.update_job_status(row_id, 'Yes') # user has worked the job.
        return row_id

    def __evaluate_job_status(self, user, row_id, response, **kwargs):
        """ """
        msg = 'deleted'
        if response == None and not row_id: # means the days has passed and the job was not confirmed.
            return None, msg
        if response == None and row_id:
            user.delete_job(row_id[1:])
            return None, msg
        if not response: # determine the type of response
            msg = 'unconfirmed'
            user.update_job_status(row_id, 'No')
        else:
            user.update_job_status(row_id, 'Yes')
            msg = 'confirmed'

        if kwargs['update']:
            create_flash_msg('A job was updated.')
            return self.__save(user, row_id, True), msg # update using the user ID
        elif not kwargs['update']:
            job_status = is_job_in_past_present_or_future(kwargs['job'], kwargs['curr_date']) # check in job is in the future or present
            if job_status == 'past' and kwargs['job'].is_shift_confirmed.lower() == 'yes':
                return self.__update_job_status(user, 'Yes'), msg
            elif job_status == 'past' and kwargs['job'].is_shift_confirmed.lower() == 'No':
                return None, 'unconfirmed'
            elif job_status  == 'present':
                if kwargs['job'].is_shift_confirmed.lower() == 'no' and is_shift_now(kwargs['job']):
                    return None, 'unconfirmed' # shift has already started
                elif kwargs['job'].is_shift_confirmed.lower() == 'no' and not is_shift_now(kwargs['job']):
                    return self.__save(user), 'not yet' # The shift has not yet started but is not confirmed yet
                elif kwargs['job'].is_shift_confirmed.lower() == 'yes' and is_shift_now(kwargs['job']):
                    return self.__save(user), 'confirmed' # user current working the shift
                elif kwargs['job'].is_shift_confirmed.lower() == 'yes' and not is_shift_now(kwargs['job']):
                    return self.__save(user), 'not yet' # shift not yet started
                elif kwargs['job'].is_shift_confirmed.lower() == 'yes' and is_shift_over(kwargs['job']):
                    return self.__update_job_status(user, 'Yes'), 'confirmed' # the current shift is now over.
            elif job_status == 'future':
                return self.__save(user), 'not yet'

    def __process_form_helper(self, user, curr_date, job, row_id=None, update=False):
        """A private helper method that helps the process form method"""

        # if update is set to true, checks whether the updated job is now active or
        # or now non-active. Non-active meaning the user has worked the shift/job
        # and it is now currently over. Active means the job/shift has not yet started.
        # If the job is now active updates the the status of job to No
        # otherwise Yes if the job is now non-active.
        response = has_previous_job_been_worked(job, curr_date, self.is_shift_confirmed.lower())
        if update:
            return self.__evaluate_job_status(user, row_id, response,
                                              update=True, job=None,
                                              curr_date=None)
        return self.__evaluate_job_status(user, row_id, response,
                                          update=False, job=job,
                                          curr_date=curr_date)

    def process_form(self, start_date, end_date, day, curr_date, job, row_id=None, update=False):
        """process_form(str, str, str, optional str, optional bool) -> return(obj or None)

        Processes the form and adds the user job details to the database.

        :parameters
           - start_date: The start date for the job (string).
           - end_date  : The ending date for the job (string).
           - day       : The day of the week the job is on.
           - returns   : Returns a row id.

        Optional flags
        -------------
        row_id: The row id corresponds to a job row in database.
        update: When update is True the old row will be updated with new data.
        """
        user = User(session['username'], start_date, end_date,
                    check_day(day), _id=session['user_id'])
        if update:
            return self.__process_form_helper(user, curr_date, job, row_id, update=True)
        return self.__process_form_helper(user, curr_date, job)
