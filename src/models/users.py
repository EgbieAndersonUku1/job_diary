# -*- coding: utf-8 -*-
##################################################################################
# Author : Egbie Uku
# The User class does not have access to the database or anything else. It
# can only access the job records of the users via the Record class API.
#################################################################################

import time
import uuid
import sys
from records import Records
from utils import translate_to_month_num, get_daily_rate, time_to_str, get_hours_worked, time_to_float


class User(object):
    """User(class)
    The User class has access to the job records. The allows the User class
    to access the job details to either update, delete, view or add all
    via an easy interface.
    """

    def __init__(self, full_name, start_date=None, end_date=None, day=None, _id=None):
        self.full_name  = full_name
        self.start_date = start_date
        self.end_date   = end_date
        self.day = day
        self.id  = uuid.uuid4().hex if _id is None else _id

        date = time.strftime("%d/%m/%Y")
        if self.start_date == None:
           self.start_date = date
        if self.end_date == None:
           self.end_date = date
        if self.day == None:
           self.day = time.strftime('%A')

    # add the job details to database
    def add_job_details(self, job_title, descr, loc, start_time, finish_time, hourly_rate):

        hours = get_hours_worked(self.start_date, start_time, self.end_date, finish_time)
        # create a new record obj add the details to it and save
        record = Records(job_title=job_title, descr=descr,
                         loc=loc,start_time=start_time,
                         finish_time=finish_time,
                         hourly_rate=hourly_rate,
                         total_hours=time_to_str(hours),
                         _hours = time_to_float(hours),
                         user_id=self.id, daily_rate=get_daily_rate(hours, hourly_rate),
                         date=self.start_date,
                         day=self.day,
                         month=self.start_date.split('/')[1])
        record.save()

    def get_by_hour(self, hours, date1=None, date2=None, month1=None,
                    month2=None, year1=None, year2=None):
        pass

    def get_by_user_id(self):
        """get_by_user_id(None) -> return(obj)
        Returns: either a single job object or multiple user object or None.
        """
        return Records.find_by_user_id(self.id)

    def get_by_row_id(self, num):
        """get_by_row_id(None) -> return(obj)
        Searches the job record by row id

        Returns: either a single job obj parameter or None.
        """
        return Records.find_by_row_id(num, self.id)

    def get_by_job_title(self, job):
        """get_by_job_title(str) -> return(obj)
        Finds jobs based on the users job title

        Returns: either a single job object or multiple user object or None.
        """
        return Records.find_by_job_title(job, self.id)

    def get_by_date_or_day(self, date=None, day=None):
        """get_by_date_and_day(str, str) -> return(str)
        Finds jobs based on the date and day

        Returns: either a single job object or multiple user object or None.
        """
        return Records.find_by_date_or_day(date, day, self.id)

    def get_by_location(self, loc):
        """get_by_location(str) -> return(obj)
        Finds jobs based on the given location
        Returns: either a single job object or multiple user object or None.
        """
        return Records.find_by_location(self.id, loc)

    def delete_row(self, row_id):
        """delete_row(str) -> return(None)
        Deletes a row from the database using the row id
        """
        return Records.delete_row(row_id, self.id)

    def update_row(self, row_id):
        """update_row(str, str) -> return(None)
        Updates a row using the row id
        """
        pass

    def get_by_amount(self, amount=None, operand=None, amount2=None, date=None, day=None):
        return Records.find_by_amount(operand, amount, amount2, date, day, self.id)

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
        return Records.find_by_month(month1, month2, self.id)

    def __repr__(self):
        return '{}'.format(self.full_name)
    # users has access Login
