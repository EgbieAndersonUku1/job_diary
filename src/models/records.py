# -*- coding: utf-8 -*-

####################################################################################
# Author : Egbie Uku
# Unlike the User class the Records class has directly access to the database and so
# can access the records of the jobs for any users. The Records class does not have
# access to the User class or anything else. Its primary job is to execute and return
# queries for the User class.
####################################################################################

import sys
import os
import random
import time
import uuid
from utils import translate_to_month_num, gen_row_id, get_hours_worked
from database import DataBase as db

class Records(object):
    """Records (class)
    The Records class has directly access to the database. It can use that access
    to either delete, retreive or update the record details of the user.
    """

    def __init__(self, job_title, descr, loc, start_time, finish_time,
                           hourly_rate, total_hours, _hours, user_id, daily_rate,
                          date, day, month, row_id=None, _id=None):

        self.job_title  = job_title
        self.descr = descr
        self.daily_rate  = daily_rate
        self.start_time  = start_time
        self.finish_time = finish_time
        self.hourly_rate = hourly_rate
        self.total_hours = total_hours # hours in words e.g 2 hrs and 10 mins
        self._hours  = _hours                 # hours in float 2.10 e.g 2 hrs and .10 mins for db comparision
        self.user_id = user_id
        self.date =  date
        self.day  =  day
        self.loc  = loc
        self.row_id = gen_row_id() if row_id is None else row_id
        self.month = month
        self._id = uuid.uuid4().hex if _id is None else _id
        self.track_times  = {}


    @classmethod
    def _find(cls, query, key, limit):
        """_find(str, str) -> return (obj or None)
        data = db.find_one(collections='jobs_details', query=query)
        A private helper function that searches the database for a value
        and returns all values that matches the users values
        """
        return [cls(**data) for data in db.search('jobs_details', query=query, key=key, limit_num=limit)]

    @classmethod
    def _find_one(cls, query):
        """A private helper function that searches the database for a value
        and returns a single value that matches the users values
        """
        return cls(**data) if data is not None else None

    @classmethod
    def find_by_job_title(cls, query, user_id, limit=None):
        """Retrieves the data using the job title"""
        query = {'job_title' : query.title(), 'user_id': user_id}
        return cls._find(query=query, key=('dates', -1), limit=limit)

    @classmethod
    def find_by_row_id(cls, row_id, user_id):
        """Retreives the job data using the row id"""
        row_id = '#' + str(row_id).strip('#')
        return cls._find_one(query={'row_id':row_id, 'user_id':user_id})

    @classmethod
    def find_by_date_or_day(cls, date, day, user_id, limit):
        """Retreives the job using the date or day"""

        key = ('daily_rate', -1)
        if date and day:
            return cls._find({'date':date, 'day':day.title(), 'user_id':user_id}, key=key, limit=limt)
        elif date and not day:
            return cls._find(query={'date': date, 'user_id': user_id}, key=key, limit=limit)
        elif day and not date:
            return cls._find(query={'day': day.title(), 'user_id':user_id}, key=key, limit=limit)

    @classmethod
    def find_by_month(cls, month, month2, user_id, limit):
        """find_by_month(str, str, str) -> return(None or obj)

        The method find_by_month receives a strings e.g. January from the User inteface.
        It then translates it into a month number since the months are stored in the database
        as numbers. (This makes it easy to query two months e.g. find days worked between
        the month January and Feb which includes the starting and ending month January
        and February.) It then uses the number to query the database for those days.
        """
        key = ('month', -1)
        if month and not month2:
            return cls._find(query={'month':translate_to_month_num(month)}) # user wants information for a single month
        elif month and month2: # user wants information between two given months

            month  = translate_to_month_num(month)  # translate month to number
            month2 = translate_to_month_num(month2) # translate month2 to number
            month, month2 = min(month, month2), max(month, month2) # ensure that month1 is less then month2

            # return days worked between the two months given including the starting and ending month
            return cls._find(query={'month': {'$gte': month, "$lte":month2},
                                    'user_id':user_id},
                                     key=key, limit=limit)

    @classmethod
    def find_by_location(cls, loc, user_id, limit):
        return cls._find(query={'loc': loc.title(),
                                'user_id':user_id},
                                key=('dates', -1), limit=limit)

    @classmethod
    def find_by_user_id(cls, user_id, limit):
        """retreives the job using the user id"""
        return cls._find({'user_id':user_id}, key=('dates', -1), limit=limit)

    # wages, bool_operation=None, amount=None, amount2=None, date=None, day=None
    @classmethod
    def find_by_amount(cls, amount=None, operand=None, amount2=None, date=None, day=None):
        """finds the job records based on amount"""
        pass

    @staticmethod
    def delete_row(row_id, user_id):
        """deletes the row using the id"""
        return db.delete_row(collections='jobs_details', query={'row_id': '#'+str(row_id), 'user_id':user_id})

    def save(self):
        """saves the data to the databases. It is saved in the form of json"""
        db.insert_one('jobs_details', self.get_json())

    def get_json(self):
        """returns a json represent of the class"""

        return { 'job_title'  : self.job_title.title(),
                 'descr'      : self.descr.title(),
                 'loc'        : self.loc.title(),
                 'start_time' : self.start_time,
                 'finish_time': self.finish_time,
                 'hourly_rate': float(self.hourly_rate),
                 'total_hours': self.total_hours,
                 '_hours'     : self._hours,
                 'user_id'    : self.user_id,
                 'daily_rate' : float(self.daily_rate),
                 'date'       : self.date,
                 'month'      : self.month,
                 'row_id'     : self.row_id,
                 'day'        : self.day,
                 '_id'        : self._id }
