# -*- coding: utf-8 -*-

####################################################################################
# Author : Egbie Uku
# Unlike the User class the Records class has directly access to the database and so
# can access the records of the jobs for any users. The Records class does not have
# access to the User class or anything else. Its primary job is to execute and return
# queries for the User class.
####################################################################################

from database import DataBase as db
from translator import translate_to_month_num, get_hours_worked
import random
import time

class Records(object):
    """Records (class)
    The Records class has directly access to the database. It can use that access
    to either delete, retreive or update the record details of the user.
    """
    def __init__(self, job_title, descr, loc, start_time, finish_time, 
                 hourly_rate, user_id, daily_rate,
                 date, day, row_id, _id, month=None):

	self.job_title = job_title
	self.descr = descr
	self.loc = loc
	self.start_time = start_time
	self.finish_time = finish_time
	self.hourly_rate = hourly_rate
	self.user_id = user_id
	self.daily_rate  = daily_rate
	self.date = time.strftime("%d/%m/%Y") if date is None else date
	self.day  = time.strftime('%A') if day is None else day
	self.month = self.date.split('/')[1] # split the date by '/' and take the month part
	self.row_id = row_id
	self._id = _id
	self.track_times  = {}

    @classmethod
    def _find(cls, query):
        """_find(str, str) -> return (obj or None)
        A private helper function that searches the database for a value
        and returns all values that matches the users values
        """
        return [cls(**data) for data in db.search('jobs_details', query=query)]

    @classmethod
    def _find_one(cls, query):
        """_find_one(str, str) -> return (obj or None)
        A private helper function that searches the database for a value
        and returns a single value that matches the users values
        """
        data = db.find_one(collections='jobs_details', query=query)
        return cls(**data) if data is not None else None

    @staticmethod
    def _gen_row_id():
        """_gen_row_id(void) -> return(str)
        A private function that generates a five digit string. This will
        be used as a row id.
        """
        return '#' + ''.join(['{}'.format(random.randint(1, 9)) for i in xrange(5)])

    @classmethod
    def find_by_job_title(cls, query):
        """Retrieves the data using the job title"""
        return cls._find(query={'job_title' : query.title()})

    @classmethod
    def find_by_row_id(cls, row_id):
        """Retreives the job data using the row id"""
        return cls._find_one(query={'row_id':row_id})

    @classmethod
    def find_by_date(cls, date):
        """Retreives the job by using the date"""
        return cls._find(query={'date': date})

    @classmethod
    def find_by_date_and_day(cls, date, day):
        """Retreives the job using the date and day"""
        return cls._find({'date':date, 'day':day.title()})

    @classmethod
    def find_by_month(cls, month, month2):
	"""find_by_month(str, str) -> return(None or obj)

	The method find_by_month receives a strings e.g. January from the User inteface.
	It then translates it into a month number since the months are stored in the database
	as numbers. (This makes it easy to query two months e.g. find days worked between
	the month January and Feb which includes the starting and ending month January
	and February.) It then uses the number to query the database for those days.
	"""
	if month and not month2:
	    return cls._find(query={'month':translate_to_month_num(month)}) # user wants information for a single month
	elif month and month2: # user wants information between two given months

	    month  = translate_to_month_num(month)  # translate month to number
	    month2 = translate_to_month_num(month2) # translate month2 to number
	    month, month2 = min(month, month2), max(month, month2) # ensure that month1 is less then month2

	    # return days worked between the two months given including the starting and ending month
	    return cls._find(query={'month': {'$gte': month, "$lte":month2}})

    @classmethod
    def find_by_location(cls, loc):
        return cls._find(query={'loc': loc.title()})

    @classmethod
    def find_by_user_id(cls, query):
        """retreives the job using the user id"""
        return cls._find(query)

    # pay, bool_operation=None, amount=None, amount2=None, date=None, day=None
    @classmethod
    def find_by_amount(cls, pay, operand, amount, amount2, date, day):
        """finds the job records based on amount"""

        boolean_values = {'>':'$gt', '<': '$lt', '<=': '$lte', '>=':'$gte', '=':'$eq'}

        if pay and not( operand and amount and amount2 and date and day):
            return cls._find(query={'daily_rate': pay})
        elif pay and date and day:
            return cls._find(query={'daily_rate':pay, 'date':date, 'day':day})
        elif pay and date:
            return cls._find(query={'daily_rate':pay, 'date':date})

        # fourth elif statement perfoms a comparision
        # Returns an amount if less than, greater than or equal to a certain
        # value amount
        # e.g  > 100 return all amount greater then 100
        # e.g < 100 return all amounts less then 100
        elif amount and operand:
            operand = boolean_values[operand]
            if day and date:
                return cls._find(query={'daily_rate': {operand:amount}, 'date': date, 'day':day})
            elif not day and date:
                return cls._find(query={'daily_rate': {operand:amount}, 'date': date})
            elif not date and day:
                return cls._find(query={'daily_rate': {operand:amount}, 'day':day})
            else:
                return cls._find(query={'daily_rate': {operand:amount}})

        # does a comparision operation between two amounts and returns all
        # values that match the specific parameters
        # e.g 400 <= 400 < 500 will return any amount between 400 and 499,
        elif amount and amount2:
            if amount > amount2:
                return cls._find(query={'daily_rate': {'$gte': amount2, "$lte":amount}})
            elif amount2 > amount:
                return cls._find(query={'daily_rate': {'$gte': amount, "$lte":amount2}})
            else:
                return cls._find(query={'daily_rate': pay})

    @staticmethod
    def delete_row(row_id):
	"""deletes the row using the id"""
	pass

    def get_daily_rate(self):
        return db.delete_row(collections='jobs_details', query={'row_id': '#'+str(row_id)})
        """calculates the daily rate"""
        pass

    def save(self):
        """saves the data to the databases. It is saved in the form of json"""
        db.insert('jobs_details', self.get_json())

    def get_json(self):
        """returns a json represent of the class"""

        return { 'job_title'  : self.job_title.title(),
                 'descr'      : self.descr.title(),
                 'loc'        : self.loc.title(),
                 'start_time' : self.start_time,
                 'finish_time': self.finish_time,
                 'hourly_rate': self.hourly_rate,
                 'daily_rate' : self.daily_rate,
		  'month'     : self.month,
                 'date'       : time.strftime("%d/%m/%Y"),
                 'day'        : time.strftime('%A'),
		 'month'      : self.month,
                 'user_id'    :self.user_id,
                 'row_id'     : self._gen_row_id()}
