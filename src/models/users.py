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
from database import DataBase as db
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
        self.end_date   = end_date  # end date needed to calculate the hours worked between start_date and end date
        self.day = day
        self.id  = uuid.uuid4().hex if _id is None else _id

    # add the job details to database
    def add_job_details(self, job_title, descr, loc, start_time, finish_time, hourly_rate):

        hours = get_hours_worked(self.start_date, start_time, self.end_date, finish_time)
        day, month, year = self.start_date.split('/')
        #self.start_date = '{}/{}/{}'.format(year, month, day) # store date in yyyy/mm/dd so that pymongo can sort data
        record = Records(job_title=job_title, descr=descr,
                         loc=loc,start_time=start_time,
                         finish_time=finish_time,
                         hourly_rate=hourly_rate,
                         total_hours=time_to_str(hours),
                         _hours = time_to_float(hours),
                         user_id=self.id, daily_rate=get_daily_rate(hours, hourly_rate),
                         date=self.start_date, # change this line
                         day=self.day,
                         end_date=self.end_date,
                         month=self.start_date.split('/')[1],
                         )
        return record.save()

    def get_by_multiple_queries(self, query, limit=0):
        """Find jobs by a multiple queries"""
        return Records.find_by_queries(query, self.id, limit=limit)

    def get_by_hours(self, hours, limit=0):
        return Records.find_by_hours_worked(hours, self.id, limit=limit)

    def get_by_user_id(self, no_of_rows):
        """get_by_user_id(None) -> return(obj)
        Returns: either a single job object or multiple user object or None.
        """
        return Records.find_by_user_id(self.id, no_of_rows)

    def get_by_row_id(self, num):
        """get_by_row_id(None) -> return(obj)
        Searches the job record by row id

        Returns: either a single job obj parameter or None.
        """
        return Records.find_by_row_id(num, self.id)

    def get_by_job_title(self, job_title, limit=0):
        """get_by_job_title(str) -> return(obj)
        Finds jobs based on the users job title

        Returns: either a single job object or multiple user object or None.
        """
        return Records.find_by_job_title(job_title, self.id, limit)

    def get_by_date_or_day(self, date=None, day=None, limit=0):
        """get_by_date_and_day(str, str) -> return(str)
        Finds jobs based on the date and day

        Returns: either a single job object or multiple user object or None.
        """
        return Records.find_by_date_or_day(date, day, self.id, limit=limit)

    def get_by_time(self, start_time=None, end_time=None, limit=0):
        """get_by_time(str, str, str) -> return(obj)
        Return the jobs based on time
        """
        return Records.get_by_time(start_time, end_time, self.id, limit=limit)

    def get_by_location(self, loc, limit=5):
        """get_by_location(str) -> return(obj)
        Finds jobs based on the given location
        Returns: either a single job object or multiple user object or None.
        """
        return Records.find_by_location(loc, self.id, limit)

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

    def get_by_daily_rate(self, daily_rate, limit=0):
        """get_by_daily_rate(str, str) -> return(obj)
        Return jobs based on the daily rate
        """
        return Records.find_by_daily_rate(float(daily_rate), limit=limit, user_id=self.id)

    def get_by_month(self, month, limit=0):
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
        return Records.find_by_month(month, self.id, limit)


    def get_records(self):
        return Records.get_records_in_json(self.id)

    def de_activate_account(self):
        pass

    def __repr__(self):
        return '{}'.format(self.full_name)
    # users has access Login
