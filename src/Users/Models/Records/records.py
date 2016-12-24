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
from src.utilities.converter import month_to_num
from src.utilities.common import gen_row_id
from src.Users.Jobs.job_helper import get_hours_worked
from src.utilities.password_hasher import create_passwd_hash
from src.utilities.common import get_questions
from src.Users.Models.Registrations.registration import Registration
from src.Users.Models.Databases.database import DataBase as db

class Record(object):
    """Records (class)
    The Records class directly access the database to either delete,
    retreive or update the job record details of the user.
    """
    def __init__(self, **kwargs):
        """Takes a list of parameters from kwargs that
        consists of the job attributes for the user and
        adds them to the database.

        :keywords parameters
            job_title  : The job title.
            descr      : The role of the job.
            loc        : The location of the job.
            start_time : The start time for the job.
            finish_time: The time the job ends.
            hourly_rate: The rate for the job.
            total_hours: (float) The total hours worked
            _hours     : The total hours worked to be
                         used only with mongodb for comparing.
            user_id    : The user id for the record.
            daily_rate : The daily rate for the job.
            date       : The date the job starts.
            end_date   : The end date for the job. Used to calcuate
                         the daily rate.
            day        : The day on the week the job is on.
            month      : The month the job is on.
            year       : Year optional parameter.
            row_id     : The row id for the table consisting of the data.
            _id        : The _id use to identify the user table.
            is_shift_confirmed: Checks if the shift has been confirmed.
                                Returns True if the shift is confirmed
                                and False othewise

        """
        self.job_title  = kwargs['job_title']
        self.descr = kwargs['descr']
        self.daily_rate  = kwargs['daily_rate']
        self.start_time  = kwargs['start_time']
        self.finish_time = kwargs['finish_time']
        self.hourly_rate = kwargs['hourly_rate']
        self.total_hours = kwargs['total_hours'] # hours in words e.g 2 hrs and 10 mins
        self._hours  = kwargs['_hours']          # hours in float 2.10 e.g 2 hrs and .10 mins for db comparision
        self.user_id = kwargs['user_id']
        self.date =  kwargs['date']
        self.end_date = kwargs['end_date']
        self.day  =  kwargs['day']
        self.loc  = kwargs['loc']
        self.year = int(self.date.split('-')[0]) if kwargs['year'] == None else kwargs['year']
        self.row_id = gen_row_id() if kwargs['row_id'] is None else kwargs['row_id']
        self.month  = kwargs['month']
        self._id = uuid.uuid4().hex if kwargs['_id'] is None else kwargs['_id']
        self.is_shift_confirmed = kwargs['is_shift_confirmed']

    def get_json(self):
        """returns a json represent of the class"""
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
                 'date'       : '{}-{}-{}'.format(self.year, self.month, self.date.split('-')[-1]), # get the day part
                 'end_date'   : '{}-{}-{}'.format(end_year, end_month, end_day),
                 'month'      : int(self.month),
                 'row_id'     : self.row_id,
                 'day'        : self.day,
                 'year'       : self.year,
                 '_id'        : self._id,
                 'is_shift_confirmed' : self.is_shift_confirmed }

    def save(self):
        """Saves the data to the databases in the form of json"""
        db.insert_one('jobs_details', self.get_json())
        return self.row_id

    @staticmethod
    def delete_row(row_id, user_id):
        """deletes the row using the id"""
        return db.delete_row(collections='jobs_details',
                             query={'row_id': '#'+str(row_id),
                             'user_id':user_id})

    @classmethod
    def find_by_user_id(cls, user_id, sort_by):
        """find_by_user_id(str) -> returns(obj or none)

        Queries the database by the user id and returns all
        jobs found in the database belonging to that user.
        Returns an obj if the there are jobs within the
        database or None if there are no jobs.

        parameters:
           - user_id: The user ID
           - sort_by: -1 sorts in descending order (10, 9, etc) and
                       1 sorts in ascending order e.g 1,2
        """
        return cls._find({'user_id':user_id}, key=('date', sort_by))

    @classmethod
    def find_by_row_id(cls, row_id, user_id):
        """find_by_row_id(str, str) -> return(obj)

        Retreives a specific job object based on the row ID.

        parameters:
           - row_id : The row number for the table.
           - user_id: The user ID.
        """
        return cls._find_one(query={'row_id':row_id, 'user_id':user_id})

    @classmethod
    def _date_range(cls, query_by, date, date_two, user_id):
        """A wrapper function that retreives the days worked between dates"""

        if query_by == 'month':
            date, date_two = int(month_to_num(date)), int(month_to_num(date_two))
            date, date_two = min(date, date_two), max(date, date_two) # ensure month1 < month2
        return cls._find(query={query_by: {'$gte': date, "$lte":date_two},
                        'user_id':user_id},
                         key=('date', -1))

    @classmethod
    def get_user_id(cls, username):
        """ """
        login_obj = cls._find_one(collection='login_credentials',
                                  query={'username': username.lower()},
                                  return_obj=False)
        return login_obj['_id']

    @classmethod
    def _find(cls, query, key):
        """_find(dict, tuple) -> return (list of obj or None)

        A private helper function that queries the database
        based on the user query. Returns a list of job objects
        that matches the users parameters or an empty list if
        the parameters do not match.

        :parameters
           - query  : The query to be used to query the database.
           - key    : Sorts the returned data based on the key.
        """
        return [cls(**data) for data in db.search('jobs_details',
                                                   query=query,
                                                   key=key,
                                                   limit_num=0)]
    @classmethod
    def _find_one(cls, collection='jobs_details', query=None, return_obj=True):
        """_find_one(dict) -> return(obj or None)

        A private helper function that queries the
        database based on the user query. It returns a single
        job object that matches the users parameter or
        None if the parameters are not matched.

        :parameters
           - query  : query to be used to query the database.
           - return_obj: If return_obj is set to True returns
                         an object else returns a dictionary.
        """
        data = db.find_one(collection, query)
        if return_obj and data != None:
            return cls(**data)
        elif not return_obj and data != None:
            return data
        return None

    @classmethod
    def find_by_date_range(cls, date, date_two, user_id):
        """find_by_date_range(str, str, str) -> return(obj or None)

        Returns the days worked between two dates
        including the starting and ending months.

        :paramaters
           - date    : starting date
           - date_two: the finishing date
           - user_id : The user id.

        >>> find_by_date_range(2016-09-10, 2016-09-12, '12548')
        [objectID('..')]
        >>> find_by_date_range(2016-09-10, 2016-09-12, '12548')
        []
        """
        return cls._date_range('date', str(date), str(date_two), user_id)

    @classmethod
    def find_by_day(cls, day, user_id):
        """find_by_day(str, str, str) -> return(obj or None)

        Queries the database by day and returns an object
        if found and none if not found.

        :parameters
           - date   : The data to query by.
           - day    : The day to query by.
           - user_id: The user ID
        """
        return cls._find(query={'day': day.title(),
                               'user_id':user_id},
                               key=('date', -1))

    @classmethod
    def find_by_date(cls, date, user_id):
        """find_by_date(str, str, str) -> return(obj or None)

        Queries the database by date and returns an object if found
        and none if not found.

        :parameters
           - date   : The data to query by.
           - day    : The day to query by.
           - user_id: The user ID
        """
        return cls._find(query={'date': date,
                                'user_id': user_id},
                                 key=('date', -1))

    @classmethod
    def find_by_year(cls, year, user_id):
        """find_by_year(str, str) -> return(None or Obj)

        Returns the query based on year.

        :parameters
            - year   : The year in which to query
            - user_id: The user ID to use for the query.
        """
        return cls._find(query={'year': int(year),
                                'user_id': user_id},
                                key=('date', -1))

    @classmethod
    def find_by_month(cls, month, user_id):
        """find_by_month(str, str) -> return(None or obj)

        Returns a single object if parameters are matched
        or none if the parameters are not matched.

        :parameters
            - month  : The month to query the database by.
            - user_id: The user ID.
        """
        return cls._find(query={'month':int(month_to_num(month)),
                                'user_id': user_id},
                                key=('date', -1))

    @classmethod
    def find_by_month_range(cls, month_one, month_two, user_id):
        """find_by_month_range(str, str, str) -> return(obj or None)

        Takes two months and returns the days worked between the
        two months. The days returned including the starting
        and ending months.

        :parameters
            - month_one: The starting month.
            - month_two: The ending month.

        >>> find_by_month(month_one, month_two, '12345')
        [obj]
        """
        return cls._date_range('month', month[0:3].title(),
                                month_two[0:3].title(), user_id)

    @classmethod
    def find_by_start_time(cls, start_time, user_id):
        """get_by_time(str, str, str) -> return(obj or None)

        Retrieives the job based on the start time.
        Returns object if found and none if not found.

        :parameters
            - start_time: The time the job started.
            - user_id  : The user id to use for the query.
        """
        return cls._find(query={'start_time': start_time,
                                'user_id': user_id},
                                key=('date', -1))

    @classmethod
    def find_by_finish_time(cls, finish_time, user_id):
        """get_by_time(str, str, str) -> return(obj or None)

        Returns the job based on the finish time.
        Returns the object or None.

        :parameter
            - finish_time: The time the job ended.
            - user_id    : The user id to used for the query.
        """
        return cls._find(query={'finish_time': finish_time,
                                'user_id': user_id},
                                 key=('date', -1))

    @classmethod
    def find_by_hours_worked(cls, hours, user_id):
        """find_by_hours_worked(str, str) -> return(obj or None)

        Queries by hours worked. Returns an object if found or
        None.

        :parameters
            - hours  : The total hours the user worked.
            - user_id: The user itself.
        """
        return cls._find(query={'_hours' : float(hours),
                                'user_id': user_id},
                                 key=('date', -1))

    @classmethod
    def find_by_job_title(cls, query, user_id):
        """find_by_job_title(dict, str) -> return(obj or None)

        Queries the database based on the job title. Returns
        an object if parameters match or None or not found.

        :parameters:
            - query  : The query to be used to query the database
            - user_id: The user ID
        """
        return cls._find(query={'job_title' : query.title(),
                                'user_id': user_id},
                                 key=('date', -1))

    @classmethod
    def find_by_daily_rate(cls, daily_rate, user_id):
        """find_by_daily_rate(str, str) -> return(obj or None)

        Queries the database based on the daily rate
        and returns an object if found and none if not.

        :parameters:
            - daily_rate: A day's pay.
        """
        return cls._find({'daily_rate': daily_rate,
                         'user_id':user_id},
                          key=('date', -1))

    @classmethod
    def find_by_location(cls, loc, user_id):
        """find_by_location(str, str) -> return(obj or None)

        Queries the database by location. Returns obj
        if found or None if not found.

        :parameters:
            - loc    : The location to query the database by.
            - user_id: The user ID
        """
        return cls._find(query={'loc': loc.title(),
                               'user_id':user_id},
                                key=('date', -1))
    @classmethod
    def update_password(cls, username, new_passwd):
        """Allows the user to update their password.
        """
        query = {"username": username, "password" : new_passwd}
        db.update(collections='login_credentials', key='password',
                        value=new_passwd, query=query)

    @classmethod
    def update(cls, row_id, form, update_row=True):
        """update(str, form_obj) -> return(str)

        Updates the old row with new information.

        :parameters
            - row_id : The row to update.
            - form   : form object containing the new info.
        """
        query = {"loc"    : form.loc.title(),
                 "_hours" : form._hours,
                 "row_id" : form.row_id,
                 "user_id": form.user_id,
                 "descr"  : form.descr.title(),
                 "finish_time" : form.finish_time,
                 "start_time" : form.start_time,
                 "month" : int(form.month),
                 "total_hours" : form.total_hours,
                 "daily_rate"  : form.daily_rate,
                 "year" : form.year,
                 "date" : form.date,
                 "end_date": form.end_date,
                 "hourly_rate" : form.hourly_rate,
                 "day" : form.day.title(),
                 "job_title" : form.job_title.title(),
                 'is_shift_confirmed': form.is_shift_confirmed}

        db.update('jobs_details', 'row_id', row_id, query)
        if update_row:
            return form.row_id

    @classmethod
    def find_by_confirmation(cls, user_id, confirmation):
        """return all jobs based on their confirmation"""
        return cls._find(query={"is_shift_confirmed": confirmation,
                               'user_id':user_id},
                                key=('date', -1))

    @classmethod
    def save_secret_answers(cls, form, user_id, username):
       """save_secret_answers(obj, str) -> return(None)

       Saves the user's secret answers for the forgotten
       password to the database.
       """
       question_one, question_two = get_questions()
       secret_answers = {'username' : username.lower() ,
                          question_one: create_passwd_hash(str(form.maiden_name.data.lower())),
                          question_two: create_passwd_hash(str(form.leisure.data.lower())),
                          'user_id': user_id }
       db.insert_one(collection='forgotten_password', data=secret_answers)

    @classmethod
    def get_secret_answers(cls, collection, query):
        """ """
        return cls._find_one(collection, query, False)

    @staticmethod
    def get_records_in_json(user_id):
        """Returns the records in the database as json"""

        query, user_records = {'user_id':user_id}, {}
        records = db.search('jobs_details',
                              query=query,
                              key=('date', -1),
                              limit_num=0) # returns a cursor not not an obj

        # creates a json object based on the data retreive from the database.
        for record in records:
            if record[u'date'] in user_records:
                user_records[record[u'date']].append(record)
            else:
                user_records[record[u'date']] = [record]
        return user_records
