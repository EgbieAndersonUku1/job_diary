import time
import uuid
from job import Job

#Login details -> User model -> Jobs Model

# user-job
class User(object):

    def __init__(self, full_name, email, password, _id=None):
        self._full_name = full_name
        self._email = email
        self.id = uuid.uuid4().hex if _id is None else _id

    def add_job_details(self, title, descr, loc, start_time, finish_time,
                        hourly_rate, daily_rate=0, _id=None,
                        curr_date=None, curr_day=None):

        job = Job(title=title, descr=descr, loc=loc, start_time=start_time,
                  finish_time=finish_time, hourly_rate=hourly_rate,
                  daily_rate=daily_rate, current_date=curr_date,
                  current_day=curr_day, user_id=self.id)
        job.save()

    def get_job_details(self):
        # return all jobs detail belong to specific email
        data_obj = Job.get_job_details(collections='jobs_details', query={'user_id': self.id})
        return [Job(**data) for data in data_obj]

    def get_by_row_id(self, num):
        return Job.find_by_row_id('#' + str(num).strip('#'))

    def delete_row(self, row_id):
        return Job.delete_row(collections='jobs_details', row_id=row_id)

    def update_row(self, date, day):
        pass

    # users has access Login
