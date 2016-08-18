from database import DataBase as db
import random

class Records(object):
    """Records (class)
    The Records class has directly access to the database. It can use that access
    to either delete, retreive or update the record details of the user.
    """
    def __init__(self, job_title, descr, loc, start_time,
                 finish_time, hourly_rate, user_id, daily_rate=0,
                 date=None, day=None, row_id=None, _id=None):

        self.job_title = job_title
        self.descr = descr
        self.loc = loc
        self.start_time = start_time
        self.finish_time = finish_time
        self.hourly_rate = hourly_rate
        self.daily_rate  = daily_rate
        self.user_id = user_id
        self._id = _id
        self.date = time.strftime("%d/%m/%Y") if date is None else date
        self.day  = time.strftime('%A') if day is None else day
        self.row_id = row_id
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
    def find_by_location(cls, loc):
        """retreives the job via the location"""
        return cls._find(query={'loc': loc.title()})

    @classmethod
    def find_by_user_id(cls, query):
        """retreives the job using the user id"""
        return cls._find(query)

    @staticmethod
    def delete_row(row_id):
        """deletes the row using the id"""
        return db.delete_row(collections='jobs_details', query={'row_id': '#'+str(row_id)})

    def get_daily_rate(self):
        """calculates the daily rate"""
        pass

    def save(self):
        """saves the data to the databases. It is saved in the form of json"""
        db.insert('jobs_details', self.get_json())

    def get_json(self):
        """returns a json represent of the class"""

        return { 'job_title': self.job_title.title(),
                 'descr': self.descr.title(),
                 'loc'  : self.loc.title(),
                 'start_time' : self.start_time,
                 'finish_time': self.finish_time,
                 'hourly_rate': self.hourly_rate,
                 'daily_rate' : self.get_daily_rate(),
                 'date':time.strftime("%d/%m/%Y"),
                 'day' :time.strftime('%A'),
                 'user_id' :self.user_id,
                 'row_id': self._gen_row_id()}
