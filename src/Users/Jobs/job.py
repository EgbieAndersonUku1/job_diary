# -*- coding: utf-8 -*-
####################################################################
# Author : Egbie Uku
# The User class access the database through the
# record class and returns the attributes of the job such
# as title, location, etc.
####################################################################

import uuid
from src.models.Records.record import Records
from src.utilities.time_processor import time_to_str, time_to_units
from src.utilities.job_processor import get_daily_rate, get_hours_worked
from src.Users.Validator.validate_secret_questions import ValidiateSecretQuestions

class Job(object):
    """User(class)
    The Job class allows the user to add, modify and
    delete jobs from database via the records class.
    """
    def __init__(self, full_name, start_date=None, end_date=None, day=None, _id=None):
        self.full_name = full_name
        self.start_date = start_date
        self.end_date = end_date
        self.day = day
        self.id = uuid.uuid4().hex if _id is None else _id

    def add_job_to_records(self, job_title, descr, loc, **kwargs):
        """add_job_to_records(str, str, str, str, str, str) -> return(obj or str)

        This method has two functions. The first primary function
        allows the user to save the job's attributes e.g title, description,
        job location to the database.

        The second function allows the user to overide an existing
        job row with new information when the flag update to True.

        :parameters
            - job_title  : The title of the job.
            - descr      : The description for the job.
            - loc        : The location for the job.

        :kwargs arguments
            - start_time : The time shift/job starting.
            - finish_time: The time shift/job is ending
            - hourly_rate: The hourly rate for the job.
            - update     : (Optional) parameter, if set to True, updates
                            the row with with the new jobs info.
            - confirm_shift: States whether the shift has been confirmed.
                            Returns True if the shift has been confirmed
                            and False otherwise.
        """
        hours = get_hours_worked(self.start_date, kwargs['start_time'],
                                 self.end_date, kwargs['finish_time'])
        units  = time_to_units(hours)    # convert hours worked to units
        record = Records(job_title=job_title,
                         descr=descr,
                         loc=loc,
                         start_time=kwargs['start_time'],
                         finish_time=kwargs['finish_time'],
                         hourly_rate=kwargs['hourly_rate'],
                         total_hours=time_to_str(hours),
                         _hours=units,
                         user_id=self.id,
                         daily_rate=get_daily_rate(units, kwargs['hourly_rate']),
                         date=self.start_date,
                         end_date=self.end_date,
                         day=self.day,
                         month=self.start_date.split('-')[1], # get the month part
                         year=None,
                         row_id=None,
                        _id=None,
                        is_shift_confirmed=kwargs['is_shift_confirmed'])
        return (record.save() if not kwargs['update'] else record) # return obj if update is true else row id

    def get_all_jobs(self, sort_by=-1):
        """get_by_user_id(int) -> return(obj)

        Returns all the jobs the users has worked
        in descending order (default).

        :parameters
           - sort_by : Takes two parameters in the form of
                       either (-1 or 1).
                      -1: Sorts in descending order
                          e.g. 10, 9, 8, 7....1
                       1: Sorts in ascending order
                          e.g. 1,2,3,4,...10
        """
        return Records.find_by_user_id(self.id, sort_by)

    def get_job_by_row_id(self, row_id):
        """get_job_by_row_id(None) -> return(obj)

        Returns a specific job row from the database in
        the form of a job object.

        :parameters
           - row_id : Searches the database using a specific
                      row id and returns a job object.
        """
        return Records.find_by_row_id(row_id, self.id)

    def get_job_by_year(self, year):
        """Returns all the jobs worked in that year"""
        return Records.find_by_year(year, self.id)

    def get_job_by_date(self, date):
        """get_job_by_date(str) -> return(str)

        Queries the records and returns all jobs
        based on a specific date. Returns a job
        object if found and None if not found.

        :parameters
           - date : Returns all the jobs worked for
                    that specific date.
        """
        return Records.find_by_date(date, self.id)

    def get_job_by_day(self, day):
        """get_by_date_and_day(str) -> return(str)

        Queries the records by a specific day and
        returns a job object containing all the jobs worked
        and none otherwise.

        :parameters
           - day : Searches the records for all
                   jobs worked on that day.
        """
        return Records.find_by_day(day, self.id)

    def get_job_by_date_range(self, date, date_two):
        """get_by_date_range(str, str) -> return(obj or None)

        Queries the records for days worked between two dates
        which include the starting date and the ending
        date. Returns a job object if the parameters
        match and None.

        parameters:
            - date: The starting date.
            - date_two: The end date.
        """
        return Records.find_by_date_range(date, date_two, self.id)

    def get_job_by_month_range(self, month_one, month_two):
        """get_job_by_month_range(str, str) -> return(obj or None)

        Return the all jobs worked between two given months.
        The jobs include the ones worked for the starting month (month_one)
        and the ones for the ending month (month_two).

        :parameters
            - month_one: The first month to query by.
            - month_two: The second month to query by.
            - returns  : Returns None or an object if
                         parameters are found.
         """
        return Records.find_by_month_range(month_one, month_two, self.id)

    def get_job_by_month(self, month):
        """get_by_month(str) -> return(None or obj)

        Queries the records for all jobs worked for a
        specific month. Returns a job object if found or None
        otherwise.

        parameters:
           - month  : The month to query by.
           - returns: A job object if found and none otherwise.
        """
        return Records.find_by_month(month, self.id)

    def get_job_by_start_time(self, start_time):
        """get_job_by_start_time(str) -> return(obj or None)

        Queries the records based on the time the job starts
        and returns a job object if found or None otherwise.

        parameters:
           - start_time: The start time to query by.
                         Time must be entered as hh:mm

        >>> get_by_start_time('11:00')
        objectID(..)
        >>> get_by_start_time('12:00')
        None
        """
        return Records.find_by_start_time(start_time, self.id)

    def get_job_by_finish_time(self, finish_time):
        """get_by_time(str) -> return(obj)

        Queries the records based on the time the job finishs
        and returns a job object if found or None.

        :parameters
           - finish_time: The ending time for the job.
                          The finish time is in the form of hh:mm.

        >>> get_by_finish_time('11:00')
        objectID(..)
        >>> get_by_finish_time('12:00')
        None
        """
        return Records.find_by_finish_time(finish_time, self.id)

    def get_by_job_hours(self, hours):
        """get_by_hours(float) -> return(obj or None)

        Queries the records based on the number of hours
        for a job. Returns a job job object if the
        parmameter match or none otherwise.

        parameters:
           - hours: Queries by hours. Hours must be entered
                    as float. For example 2 hrs and 10 mins
                    must be entered as 2.10.

        >>> get_by_hours(2.10)
        objectID(...)
        """
        return Records.find_by_hours_worked(hours, self.id)

    def get_by_job_title(self, job_title):
        """get_by_job_title(str) -> return(obj or none)

        Queries the records by the job title and returns
        a list of job object that match the job title.
        Returns None if the parameter for the jobs are
        not matched and job object otherwise.

        parameters:
           - job_title : The job title to query by.
           - returns   : A list of job obect that match
                         the job title parameter or
                         none otherwise.
        """
        return Records.find_by_job_title(job_title, self.id)

    def get_by_daily_rate(self, daily_rate):
        """get_by_daily_rate(float) -> return(obj or none)

        Queries the records by the total daily rate for the job
        and returns a job object if found or None.

        parameters:
          - daily_rate: The daily rate (float) to query by.
          - returns   : A job object if found or None otherwise.
        """
        return Records.find_by_daily_rate(float(daily_rate), user_id=self.id)

    def get_by_job_location(self, loc):
        """get_by_location(str) -> return(obj)

        Queries the records by location of the job
        and returns a job object if found or None.

        parameters:
            - loc: The location of job to query by.
            - returns: An object if found and none otherwise.
        """
        return Records.find_by_location(loc, self.id)

    def to_json(self):
        """return the records in json format."""
        return Records.get_records_in_json(self.id)

    def delete_job(self, row_id):
        """delete_job_row(str) -> return(None)
        Deletes a job row from the database using the row id.

        parameters:
           - row_id: The job row to delete.
        """
        Records.delete_row(row_id, self.id)
        return ''

    def update_job(self, row_id, form):
        """update_job_row(str, obj) -> return(None)

        Updates a particular job row with new information.

        parameters:
           - row_id: The row id assigin to a job within a database.
           - form  : Form object contains the new
                     data to update the old row with.
        """
        return Records.update(row_id, form)

    def get_job_by_confirmation(self, confirmation):
        """get_job_by_confirmation(str) -> return(obj or None)

        Returns all job that either confirmed or not confirmed.

        :parameters
           - confirmation : either 'yes' or 'no'.

        >>> get_by_confirmation('yes')
        objectID(...)
        >>> get_by_confirmation('no')

        """
        return Records.find_by_confirmation(self.id, confirmation)

    def send_jobs_by_email(self):
        """Sends the latest jobs by email. That is
        jobs that are starting on the current working
        day.
        """
        pass

    def __repr__(self):
        return '{}'.format(self.full_name)
