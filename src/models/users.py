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
    The User class allows the user to add, modify and delete jobs from database
    via the records class.
    """
    def __init__(self, full_name, start_date=None, end_date=None, day=None, _id=None):
        self.full_name  = full_name
        self.start_date = start_date
        self.end_date   = end_date  #
        self.day = day
        self.id  = uuid.uuid4().hex if _id is None else _id

    def add_job_details(self, job_title, descr, loc, start_time, finish_time, hourly_rate):
        """add_job_details(str, str, str, str, str, str) -> return(None)

        Takes the attributes of a job such as the title, the job description,
        the job location, the hourly rate, the start and finish time and saves
        it to the database.
        """
        hours = get_hours_worked(self.start_date, start_time, self.end_date, finish_time) # calculate the hours worked
        daily_rate = get_daily_rate(hours, hourly_rate) # calculate the daily rate
        day, month, year = self.start_date.split('/')

        record = Records(job_title=job_title, descr=descr,
                         loc=loc,start_time=start_time,
                         finish_time=finish_time,
                         hourly_rate=hourly_rate,
                         total_hours=time_to_str(hours),
                         _hours = time_to_float(hours),
                         user_id=self.id, daily_rate=daily_rate,
                         date=self.start_date,
                         day=self.day.replace('0', ''),
                         end_date=self.end_date,
                         month=month.replace('0', ''))
        return record.save()

    def get_by_hours(self, hours):
        """get_by_hours(int) -> return(obj or None)
        Queries the records by hours and returns a job obj if found or None.
        """
        return Records.find_by_hours_worked(hours, self.id)

    def get_by_user_id(self):
        """get_by_user_id(None) -> return(obj)
        Queries the records by user id and returns a job obj.
        """
        return Records.find_by_user_id(self.id)

    def get_by_row_id(self, num):
        """get_by_row_id(None) -> return(obj)
        Queries the records by row and returns a job obj.
        """
        return Records.find_by_row_id(num, self.id)

    def get_by_job_title(self, job_title):
        """get_by_job_title(str) -> return(obj)
        Queries the records by job title and returns a job obj if found or None.
        """
        return Records.find_by_job_title(job_title, self.id)

    def get_by_date_or_day(self, date=None, day=None):
        """get_by_date_and_day(str, str) -> return(str)
        Queries the records by either date or day and returns a job obj if found or None.
        """
        return Records.find_by_date_or_day(date, day, self.id)

    def get_by_time(self, start_time=None, end_time=None):
        """get_by_time(str, str, str) -> return(obj)
        Queries the records by times and returns a job obj if found or None.
        """
        return Records.get_by_time(start_time, end_time, self.id)

    def get_by_location(self, loc):
        """get_by_location(str) -> return(obj)
        Queries the records by location and returns a job obj if found or None.
        """
        return Records.find_by_location(loc, self.id)

    def delete_row(self, row_id):
        """delete_row(str) -> return(None)
        Deletes a row from the database using the row id.
        """
        return Records.delete_row(row_id, self.id)

    def update_row(self, row_id):
        """update_row(str, str) -> return(None)
        Updates a row using the row id
        """
        # WRITE CODE HERE TO UPDATES ROWS
        pass

    def get_by_daily_rate(self, daily_rate):
        """get_by_daily_rate(str) -> return(obj)
        Queries the records by the daily rate and returns a job obj if found or None.
        """
        return Records.find_by_daily_rate(float(daily_rate), user_id=self.id)

    def get_by_month(self, month):
        """get_by_month(str, str(optional)) -> return(None or obj)
        Queries the records by month and returns a job obj if found or None.
        """
        return Records.find_by_month(month, self.id)

    def get_records(self):
        """return the records in json format"""
        return Records.get_records_in_json(self.id)

    def get_by_month_range(self, month, month_two):
        """Return the dates worked between month one and month 2 including
        the month one and month2"""
        return Records.find_by_month_range(month, month_two, self.id)


    def de_activate_account(self):
        """alllows the person to delete their account along with all their data"""
        pass

    def __repr__(self):
        return '{}'.format(self.full_name)
