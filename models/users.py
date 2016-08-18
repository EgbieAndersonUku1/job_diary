import time
import uuid
from records import Records

#Login details -> User model -> Jobs Model

# user-job
class User(object):
    """User(class)
    The User class has access to the job records. The allows the User class
    to access the job details to either update, delete, view or add all
    via an easy interface.
    """

    def __init__(self, full_name, email, password, _id=None):
        self.full_name = full_name
        self.email = email
        self.password = password
        self.id = uuid.uuid4().hex if _id is None else _id

    # add the job details to database
    def add_job_details(self, job_title, descr, loc, start_time, finish_time,
                        hourly_rate, daily_rate=0, curr_date=None, curr_day=None):

        # create a new record obj add the details to it and save
        record = Records(job_title=job_title, descr=descr, loc=loc,
                         start_time=start_time,finish_time=finish_time,
                         hourly_rate=hourly_rate, daily_rate=daily_rate,
                         date=curr_date, day=curr_day, user_id=self.id)
        record.save()

    def get_by_user_id(self):
        """get_by_user_id(None) -> return(obj)
        Returns: either a single job object or multiple user object or None.
        """
        return Records.find_by_user_id(query={'user_id':self.id})

    def get_by_row_id(self, num):
        """get_by_row_id(None) -> return(obj)
        Searches the job record by row id

        Returns: either a single job obj parameter or None.
        """
        return Records.find_by_row_id('#' + str(num).strip('#'))

    def get_by_job_title(self, job):
        """get_by_job_title(str) -> return(obj)
        Finds jobs based on the users job title

        Returns: either a single job object or multiple user object or None.
        """
        return Records.find_by_job_title(job)

    def get_by_date(self, date):
        """get_by_date(str) -> return(obj)
        Finds jobs based on the date

        Returns: either a single job object or multiple user object or None.
        """
        return Records.find_by_date(date)

    def get_by_date_and_day(self, date, day):
        """get_by_date_and_day(str, str) -> return(str)
        Finds jobs based on the date and day

        Returns: either a single job object or multiple user object or None.
        """
        return Records.find_by_date_and_day(date, day)

    def get_by_location(self, loc):
        """get_by_location(str) -> return(obj)
        Finds jobs based on the given location

        Returns: either a single job object or multiple user object or None.
        """
        return Records.find_by_location(loc)

    def delete_row(self, row_id):
        """delete_row(str) -> return(None)
        Deletes a row from the database using the row id
        """
        return Records.delete_row(row_id)

    def update_row(self, row_id):
        """update_row(str, str) -> return(None)
        Updates a row using the row id
        """
        pass

    def __repr__(self):
        return '{}'.format(self.full_name)
    # users has access Login
