from database import DataBase as db
import time
import random

class Job(object):

    def __init__(self, title, descr, loc, start_time,
                 finish_time, hourly_rate, user_id, daily_rate=0, _id=None,
                 current_date=None, current_day=None, row_id=None):

        self.title = title
        self.descr = descr
        self.loc = loc
        self.start_time = start_time
        self.finish_time = finish_time
        self.hourly_rate = hourly_rate
        self.daily_rate  = daily_rate
        self._id = _id
        self.user_id = user_id
        self.current_date = time.strftime("%d/%m/%Y") if current_date is None else current_date
        self.current_day  = time.strftime('%A') if current_day is None else current_day
        self.row_id = row_id
        self.track_times  = {}

    @staticmethod
    def _get_row_id():
        return '#' + ''.join(['{}'.format(random.randint(1, 9)) for i in xrange(5)])

    @staticmethod
    def find_by_row_id(row_id):
        data = db.find_one(collections='jobs_details', query={'row_id':row_id})
        return Job(**data) if data is not None else None

    @staticmethod
    def get_all(collections, query):
        return db.search(collections, query)

    @staticmethod
    def delete_row(collections, row_id):
        return db.delete_row(collections, query={'row_id': '#'+str(row_id)})

    def get_daily_rate(self):
        return 1

    def get_json(self):
        return { 'title': self.title.title(),
                 'descr': self.descr.title(),
                 'loc'  : self.loc.title(),
                 'start_time' : self.start_time,
                 'finish_time': self.finish_time,
                 'hourly_rate': self.hourly_rate,
                 'daily_rate' : self.get_daily_rate(self.start_time, self.finish_time, self.hourly_rate),
                 'current_date':time.strftime("%d/%m/%Y"),
                 'current_day' :time.strftime('%A'),
                 'user_id' :self.user_id,
                 'row_id': self._get_row_id()}

    def save(self):
        db.insert('jobs_details', self.get_json())
