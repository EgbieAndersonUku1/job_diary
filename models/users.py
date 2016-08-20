# -*- coding: utf-8 -*-

import time
import uuid
from records import Records
from translator import translate_to_month_num

#Login details -> User model -> Jobs Model

# user-job
class User(object):
    """User(class)
    The User class has access to the job records. The allows the User class
    to access the job details to either update, delete, view or add all
    via an easy interface.
    """

    def __init__(self, full_name, email, password, _id=None):
        self.full_name = full_name
        self.email = email
        self.password = password
        self.id = uuid.uuid4().hex if _id is None else _id

    # add the job details to database
    def add_job_details(self, job_title, descr, loc, start_time, finish_time,
                        hourly_rate, daily_rate=0, curr_date=None, curr_day=None,):

        # create a new record obj add the details to it and save
        record = Records(job_title=job_title, descr=descr, loc=loc,
                         start_time=start_time,finish_time=finish_time,
                         hourly_rate=hourly_rate, user_id=self.id,
                         daily_rate=daily_rate, date=curr_date,
                         day=curr_day, row_id=None, _id=None)
        record.save()

    def get_by_user_id(self):
        """get_by_user_id(None) -> return(obj)
        Returns: either a single job object or multiple user object or None.
        """
        return Records.find_by_user_id(query={'user_id':self.id})

    def get_by_row_id(self, num):
        """get_by_row_id(None) -> return(obj)
        Searches the job record by row id

        Returns: either a single job obj parameter or None.
        """
        return Records.find_by_row_id('#' + str(num).strip('#'))

    def get_by_job_title(self, job):
        """get_by_job_title(str) -> return(obj)
        Finds jobs based on the users job title

        Returns: either a single job object or multiple user object or None.
        """
        return Records.find_by_job_title(job)

    def get_by_date(self, date):
        """get_by_date(str) -> return(obj)
        Finds jobs based on the date

        Returns: either a single job object or multiple user object or None.
        """
        return Records.find_by_date(date)

    def get_by_date_and_day(self, date, day):
        """get_by_date_and_day(str, str) -> return(str)
        Finds jobs based on the date and day

        Returns: either a single job object or multiple user object or None.
        """
        return Records.find_by_date_and_day(date, day)

    def get_by_location(self, loc):
        """get_by_location(str) -> return(obj)
        Finds jobs based on the given location

        Returns: either a single job object or multiple user object or None.
        """
        return Records.find_by_location(loc)

    def delete_row(self, row_id):
        """delete_row(str) -> return(None)
        Deletes a row from the database using the row id
        """
        return Records.delete_row(row_id)

    def update_row(self, row_id):
        """update_row(str, str) -> return(None)
        Updates a row using the row id
        """
        pass

    def get_by_amount(self, pay=None, operand=None, amount=None,
                        amount2=None, date=None, day=None):
        return Records.find_by_amount(pay, operand, amount, amount2, date, day)

    def get_by_month(self, month1, month2=None):
        """get_by_month(str, str(optional)) -> return(None or obj)

        month1: The month to query by.
        month2: The optional parameter month to query by.
        returns: Either a single object, multiple obj or None if no records are found.

        If month1 is given and not month2 returns all days that the user worked
        in month1 and None if no days were worked.

        If month1 and month2 is given returns the days that user worked between
        month1 and month2 including any days worked in month1 and month2. None
        if no days are worked.

        e.g if January and June is given as month1 and month2:
        returns any days that were worked in Jan, Feb, Mar, Apr and June.

        e.g if Jan and june is given but the user did not work the entire of mar
        and Apr then the days worked in Jan, Feb, May, Jun would be returned.
        """
        return Records.find_by_month(month1, month2)

    def __repr__(self):
        return '{}'.format(self.full_name)
    # users has access Login
