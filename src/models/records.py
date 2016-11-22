# -*- coding: utf-8 -*-
####################################################################################
# Author : Egbie Uku
# class  : Record class
####################################################################################

import sys
import os
import random
import time
import uuid
from src.utilities.date_month_day_processor import month_to_num
from src.utilities.common import gen_row_id
from src.utilities.job_processor import get_hours_worked
from database import DataBase as db

class Records(object):
    """Records (class)
    The Records class directly access the database to either delete,
    retreive or update the job record details of the user.
    """
    def __init__(self, job_title, descr, loc, start_time, finish_time,
                 hourly_rate, total_hours, _hours, user_id, daily_rate,
                 date, end_date, day, month, year=None, row_id=None, _id=None):

        self.job_title  = job_title
        self.descr = descr
        self.daily_rate  = daily_rate
        self.start_time  = start_time
        self.finish_time = finish_time
        self.hourly_rate = hourly_rate
        self.total_hours = total_hours # hours in words e.g 2 hrs and 10 mins
        self._hours  = _hours          # hours in float 2.10 e.g 2 hrs and .10 mins for db comparision
        self.user_id = user_id
        self.date =  date
        self.end_date = end_date
        self.day  =  day
        self.loc  = loc
        self.year = int(self.date.split('-')[0]) if year == None else year
        self.row_id = gen_row_id() if row_id is None else row_id
        self.month  = month
        self._id = uuid.uuid4().hex if _id is None else _id

    def get_json(self):
        """returns a json represent of the class"""

        year, month, day = self.date.split('-')
        end_year, end_month, end_day = self.end_date.split('-')
        return { 'job_title'  : self.job_title.title(),
                 'descr'      : self.descr.title(),
                 'loc'        : self.loc.title(),
                 'start_time' : self.start_time,
                 'finish_time': self.finish_time,
                 'hourly_rate': float(self.hourly_rate),
                 'total_hours': self.total_hours,
                 '_hours'     : self._hours,
                 'user_id'    : str(self.user_id),
                 'daily_rate' : float(self.daily_rate),
                 'date'       : '{}-{}-{}'.format(year, month, day),
                 'end_date'   : '{}-{}-{}'.format(end_year, end_month, end_day),
                 'month'      : int(self.month),
                 'row_id'     : self.row_id,
                 'day'        : self.day,
                 'year'       : self.year,
                 '_id'        : self._id }

    def save(self):
        """Saves the data to the databases in the form of json"""
        db.insert_one('jobs_details', self.get_json())
        return self.row_id

    @staticmethod
    def delete_row(row_id, user_id):
        """deletes the row using the id"""
        return db.delete_row(collections='jobs_details', query={'row_id': '#'+str(row_id), 'user_id':user_id})

    @classmethod
    def find_by_user_id(cls, user_id):
        """find_by_user_id(str) -> returns(obj or none)

        @params:
        user_id: The user ID
        returns: An obj if the there are jobs within the database or None if there are no jobs.

        Queries the database by the user id and returns all jobs find in the database in the form
        of an object.
        """
        return cls._find({'user_id':user_id}, key=('date', -1))

    @classmethod
    def find_by_row_id(cls, row_id, user_id):
        """find_by_row_id(str, str) -> return(obj)

        @params:
        row_id : The row number for the table.
        user_id: The user ID.
        returns: A job object.

        Retreives a specific job object based on the row ID.
        """
        return cls._find_one(query={'row_id':row_id, 'user_id':user_id})

    @classmethod
    def _date_range(cls, query_by, date, date_two, user_id):
        """A helper function that retreives the days worked between dates"""

        if query_by == 'month':
            date, date_two = int(month_to_num(date)), int(month_to_num(date_two)) # translate month2 to number
            date, date_two = min(date, date_two), max(date, date_two) # ensure that month1 is less then month2
        return cls._find(query={query_by: {'$gte': date, "$lte":date_two},
                        'user_id':user_id}, 
                         key=('date', -1))
    @classmethod
    def _find(cls, query, key):
        """_find(dict, tuple) -> return (list of objects or an empty list)

        @params:
        query  : The query to be used to query the database.
        key    : Sorts the returned data based on the key.
        returns: Returns either an obj if the query is matched or None if it is not.

        A private helper function that queries the database based on the user query.
        Returns a list of job objects that matches the users parameters or an
        empty list if the parameters do not match.
        """
        return [cls(**data) for data in db.search('jobs_details', query=query, key=key, limit_num=0)]

    @classmethod
    def _find_one(cls, query):
        """_find_one(dict) -> return(obj or None)

        @params:
        query  : The query to be used to query the database
        returns: A single object if parameter is matched and none otherwise

        A private helper function that queries the database based on the user
        query. It returns a single job object that matches the users parameter or
        None if the parameters are not matched.
        """
        data = db.find_one('jobs_details', query)
        return cls(**data) if data is not None else None

    @classmethod
    def find_by_date_range(cls, date, date_two, user_id):
        """find_by_date_range(str, str, str) -> return(obj or None)

        @parmas :
        date    : starting date
        date_two: the finishing date
        user_id : The user id.

        Returns the days worked between two dates including the starting and ending months
        """
        return cls._date_range('date', str(date), str(date_two), user_id)

    @classmethod
    def find_by_day(cls, day, user_id):
        """find_by_date_or_day(str, str, str) -> return(obj or None)

        @params:
        date   : The data to query by.
        day    : The day to query by.
        user_id: The user ID
        returns: an obj if the parameter are matched or None if it is not

        Retreives the job by either date or day.
        """
        return cls._find(query={'day': day.title(), 'user_id':user_id}, key=('date', -1))

    @classmethod
    def find_by_date(cls, date, user_id):
        """find_by_date_or_day(str, str, str) -> return(obj or None)

        @params:
        date   : The data to query by.
        day    : The day to query by.
        user_id: The user ID
        returns: an obj if the parameter are matched or None if it is not

        Retreives the job by either date or day.
        """
        return cls._find(query={'date': date, 'user_id': user_id}, key=('date', -1))
       
    @classmethod
    def find_by_year(cls, year, user_id):
        """find_by_year(str, str) -> return(None or Obj)

        @params :
        year    : The year in which to query
        returns : Returns the days worked based on the year

        Queroes the database based on the year and returns a job object if found
        and None if none
        """
        return cls._find({'year': int(year), 'user_id': user_id}, key=('date', -1))

    @classmethod
    def find_by_month(cls, month, user_id):
        """find_by_month(str, str) -> return(None or obj)

        @params:
        month  : The month to query the database by.
        user_id: The user ID.
        returns: A single object if parameter is matched and none otherwise.

        Retreive the jobs based on the month worked.
        """
        return cls._find(query={'month':int(month_to_num(month)), 'user_id': user_id}, key=('date', -1))

    @classmethod
    def find_by_month_range(cls, month, month_two, user_id):
        """find_by_month_range(str, str, str) -> return(obj or None)

        @params  :
        month    : The starting month
        month_two: The ending month
        returns  : An obj if the parameter are matched and None if not matched.

        Takes two months and returns the days worked between the months
        including the starting and ending months.
        """
        return cls._date_range('month', month[0:3].title(), month_two[0:3].title(), user_id)
        
    @classmethod
    def find_by_start_time(cls, start_time, user_id):
        """get_by_time(str, str, str) -> return(obj or None)

        @params    :
        start_time : The time the job started
        returns    : An obj if the parameter are matched and None if is not matched.

        Retreive the jobs based on either the start or end time.
        """
        return cls._find(query={'start_time': start_time, 'user_id': user_id}, key=('date', -1))
        
    @classmethod
    def find_by_finish_time(cls, finish_time, user_id):
        """get_by_time(str, str, str) -> return(obj or None)

        @params    :
        finish_time : The time the job ended.
        returns    : An obj if the parameter are matched and None if is not matched.

        Retreive the jobs based on either the start or end time.
        """
        return cls._find(query={'finish_time': finish_time, 'user_id': user_id}, key=('date', -1))
        
    @classmethod
    def find_by_hours_worked(cls, hours, user_id):
        """find_by_hours_worked(str, str) -> return(obj or None)

        @params:
        hours  : The total hours the user worked.
        user_id: The user id.
        returns: A single object if parameter is matched and none otherwise

        Retreives the jobs based on the total hours the user worked.
        """
        return cls._find(query={'_hours' : hours, 'user_id': user_id}, key=('date', -1))

    @classmethod
    def find_by_job_title(cls, query, user_id):
        """find_by_job_title(dict, str) -> return(obj or None)

        @params:
        query  : The query to be used to query the database
        user_id: The user ID
        returns: A single object if parameter is matched and none otherwise

        Retreives the data based on the job title.
        """
        return cls._find(query={'job_title' : query.title(), 'user_id': user_id}, key=('date', -1))
    
    @classmethod
    def find_by_daily_rate(cls, daily_rate, user_id):
        """find_by_daily_rate(str, str) -> return(obj or None)

        @params   :
        daily_rate: A day's pay.
        user_id   : The user id.
        returns   : An obj if the there are jobs within the database or None if there are no jobs.

        Queries the database based on the daily rate and returns an object if found
        and none if not.
        """
        return cls._find({'daily_rate': daily_rate, 'user_id':user_id}, key=('date', -1))

    @classmethod
    def find_by_location(cls, loc, user_id):
        """find_by_location(str, str) -> return(obj or None)

        @params:
        loc    : The location to query the database by.
        user_id: The user ID
        returns: An obj if the parameter are matched and None if not matched.

        Queries the database by the job location.
        """
        return cls._find(query={'loc': loc.title(),'user_id':user_id}, key=('date', -1))
   
    @classmethod
    def update_row(cls, row_id, form):
        """update_row(str, form_obj) -> return(str)

        @params :
        row_id  : The row to update.
        form    : form object.
        returns : new row_id for redirection.

        Updates the old row with information from the new row.
        """
        query = {"loc"    : form.loc.title(),
                 "_hours" : form._hours,
                 "row_id" : form.row_id,
                 "user_id": form.user_id,
                 "descr"  : form.descr.title(),
                 "finish_time" : form.finish_time,
                 "start_time" : form.start_time,
                 "month" : form.month.title(),
                 "total_hours" : form.total_hours,
                 "daily_rate"  : form.daily_rate,
                 "year" : form.year,
                 "date" : form.date,
                 "end_date": form.end_date,
                 "hourly_rate" : form.hourly_rate,
                 "day" : form.day.title(),
                 "job_title" : form.job_title.title()}

        db.update_row('jobs_details', row_id, query)
        return form.row_id

    @staticmethod
    def get_records_in_json(user_id):
        """Returns the record in the database albert in the form of a json object"""

        query, user_records = {'user_id':user_id}, {}
        records = db.search('jobs_details', query=query, key=('date', -1), limit_num=0) # returns a cursor not not an obj
        
        # creates the json object based on the data retreive from the database.
        for record in records:
            if record[u'date'] in user_records:
                user_records[record[u'date']].append(record)
            else:
                user_records[record[u'date']] = [record]
        return user_records
