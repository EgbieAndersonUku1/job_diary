# -*- coding: utf-8 -*-
##################################################################################
# Author : Egbie Uku
# The User class access the database through the record class and returns
# the attributes of the job such as title, location, etc.
#################################################################################

import time
import uuid
import sys
from records import Records
from database import DataBase as db
from src.utilities.date_month_day_processor import month_to_num
from src.utilities.time_processor import time_to_str, time_to_units
from src.utilities.job_processor import get_daily_rate, get_hours_worked

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

    def add_job_details(self, job_title, descr, loc, start_time, finish_time, hourly_rate, update=False):
        """add_job_details(str, str, str, str, str, str) -> return(None)

        Takes the attributes of a job such as the title, the job description,
        the job location, the hourly rate, the start and finish time and saves
        it to the database.
        """
        hours = get_hours_worked(self.start_date, start_time, self.end_date, finish_time) # calculate the hours worked
        units = time_to_units(hours)    # convert hours worked to units
        record = Records(job_title=job_title, descr=descr,
                         loc=loc,start_time=start_time,
                         finish_time=finish_time,
                         hourly_rate=hourly_rate,
                         total_hours=time_to_str(hours),
                         _hours = units,
                         user_id=self.id, 
                         daily_rate=get_daily_rate(units, hourly_rate),
                         date=self.start_date,
                         end_date=self.end_date,
                         day=self.day,
                         month=self.start_date.split('-')[1] # get the month part of the date
                         ) 
        return (record.save() if not update else record) # returns row_id if update is true else obj
           
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

    def get_by_year(self, year):
        """Returns the days worked based on the year"""
        return Records.find_by_year(year, self.id)

    def get_by_date(self, date):
        """get_by_date_and_day(str, str) -> return(str)
        Queries the records by either date or day and returns a job obj if found or None.
        """
        return Records.find_by_date(date, self.id)

    def get_by_day(self, day):
        """get_by_date_and_day(str, str) -> return(str)
        Queries the records by either date or day and returns a job obj if found or None.
        """
        return Records.find_by_day(day, self.id)

    def get_by_date_range(self, date, date_two):
        """Returns the days worked between two dates including date and date two"""
        return Records.find_by_date_range(date, date_two, self.id)

    def get_by_month_range(self, month, month_two):
        """Return the days worked between two months including the month one and month2"""
        return Records.find_by_month_range(month, month_two, self.id)

    def get_by_month(self, month):
        """get_by_month(str, str(optional)) -> return(None or obj)
        Queries the records by month and returns a job obj if found or None.
        """
        return Records.find_by_month(month, self.id)

    def get_by_start_time(self, start_time):
        """get_by_time(str) -> return(obj)
        Queries the records by start time and returns a job obj if found or None.
        """
        return Records.find_by_start_time(start_time, self.id)

    def get_by_finish_time(self, finish_time):
        """get_by_time(str) -> return(obj)
        Queries the records by finsih time and returns a job obj if found or None.
        """
        return Records.find_by_finish_time(finish_time, self.id)

    def get_by_hours(self, hours):
        """get_by_hours(int) -> return(obj or None)
        Queries the records by hours and returns a job obj if found or None.
        """
        return Records.find_by_hours_worked(hours, self.id)

    def get_by_job_title(self, job_title):
        """get_by_job_title(str) -> return(obj)
        Queries the records by job title and returns a job obj if found or None.
        """
        return Records.find_by_job_title(job_title, self.id)

    def get_by_daily_rate(self, daily_rate):
        """get_by_daily_rate(str) -> return(obj)
        Queries the records by the daily rate and returns a job obj if found or None.
        """
        return Records.find_by_daily_rate(float(daily_rate), user_id=self.id)

    def get_by_location(self, loc):
        """get_by_location(str) -> return(obj)
        Queries the records by location and returns a job obj if found or None.
        """
        return Records.find_by_location(loc, self.id)

    def get_records(self):
        """return the records in json format"""
        return Records.get_records_in_json(self.id)
    
    def de_activate_account(self):
        """alllows the person to delete their account along with all their data"""
        pass

    def delete_row(self, row_id):
        """delete_row(str) -> return(None)
        Deletes a row from the database using the row id.
        """
        return Records.delete_row(row_id, self.id)

    def update_row(self, row_id, form):
        """update_row(str, str) -> return(None)
        Updates a row using the row id
        """
        return Records.update_row(row_id, form)

    def __repr__(self):
        return '{}'.format(self.full_name)
