#####################################################################
# Author = Egbie Uku
#####################################################################

from flask import session
from src.Users.user import User
from datetime import datetime
from src.Users.Validator.validate_date import check_day, check_date
from src.utilities.converter import month_to_num, time_to_str
from src.Users.Jobs.job_processor import get_hours_worked
from src.Users.Models.Registrations.registration import Registration
import cgi

# Process the search form.
class ValidateSearchForm(object):
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
        self.confirmation = form.job_confirmation.data
        self._user = User(session['username'], _id=session['user_id'])
        self.days = {'Mon': 'Monday', 'Tue': 'Tuesday',
                     'Wed': 'Wednesday','Thu':'Thursday',
                     'Fri': 'Friday', 'Sat': 'Saturday',
                     'Sun': 'Sunday'}

    def _is_date_str(self, date):
        """Returns True if date is in word format or False if date is in YYYY-MM-DD"""
        return date.isalpha()

    def process_dates(self, val, val2):
        """turn the dates into their month representives"""
        if self._is_date_str(val) and self._is_date_str(val2):
            if month_to_num(val[:3].title()) and month_to_num(val2[:3].title()):
                return self._user.get_by_month_range(val, val2)
        elif not self._is_date_str(val) and not self._is_date_str(val2):
            return self._user.get_job_by_date_range(val, val2)

    def get_data(self):
        """retreive and process the data from the search form template"""
        if self.job_title:
            return self._user.get_by_job_title(self.job_title.title())
        elif self.location:
            return self._user.get_by_job_location(self.location)
        elif self.date:
            return self._user.get_job_by_date(str(self.date))
        elif self.day and check_day(self.day):
            return self._user.get_job_by_day(self.days.get(self.day.title()[:3], None))
        elif self.start_time:
            return self._user.get_job_by_start_time(str(self.start_time))
        elif self.finish_time:
            return self._user.get_job_by_finish_time(str(self.finish_time))
        elif self.hrs_worked:
            return self._user.get_by_job_hours(self.hrs_worked)
        elif self.month and month_to_num(self.month[0:3].title()):
            return self._user.get_job_by_month(str(self.month[0:3].title()))
        elif self.daily_rate:
            return self._user.get_by_daily_rate(self.daily_rate)
        elif self.val_one and self.val_two:
            return self.process_dates(self.val_one, self.val_two)
        elif self.year:
            return self._user.get_job_by_year(self.year)
        elif self.confirmation:
            return self._user.get_job_by_confirmation(self.confirmation.lower())
