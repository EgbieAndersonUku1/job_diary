# -*- coding: utf-8 -*-
###################################################################
# Author : Egbie Uku
# The Job class allows the user to add, modify and
# delete jobs from records.
###################################################################

import uuid
from src.Users.Models.Records.records import Record
from src.utilities.converter import time_to_str, time_to_units
from src.Users.Jobs.job_processor import get_daily_rate, get_hours_worked

class Job(object):
    """Job:(Class).
    The Job class allows the user to add, modify and delete jobs from database.
    """
    def __init__(self, full_name, start_date=None, end_date=None, day=None, _id=None):
        self.full_name = full_name
        self.start_date = start_date
        self.end_date = end_date
        self.day = day
        self.id = uuid.uuid4().hex if _id is None else _id

    def add_job_to_records(self, job_title, descr, loc, **kwargs):
        """add_job_to_records(str, str, str, **kwargs) -> Returns(str)

        This method has two primary functions. The first allows
        the user to add/save the new job's details e.g title,
        description, job location to the database table.

        The second function allows the user to overide an existing
        data within a particular job row or field with new job
        information. This can only be done when the flag update is
        set to True.

        Returns a row id.

        :parameters
            - job_title  : The title of the job.
            - descr      : The description for the job.
            - loc        : The location for the job.

        :kwargs arguments
            - start_time : The time shift/job is starting.
            - finish_time: The time shift/job is ending
            - hourly_rate: The hourly rate for the job.
            - update     : (Optional: default False) parameter.
                           If set to True allows updating to be done
                           on a specific row.
            - row_id     : Default (None). The row_id is a string.
                           When the 'update' flag is set to True
                           and coupled with the row_id enables
                           the old data in that row to be overidden
                           with new data.
            - confirm_shift: A parameter which is either 'yes' or 'no'.
                            Yes meaning the job was confirmed and no
                            meaning the job was not confirmed.
        """
        hours = get_hours_worked(self.start_date, kwargs['start_time'],
                                 self.end_date, kwargs['finish_time'])
        units  = time_to_units(hours)    # convert hours worked to units
        record = Record(job_title=job_title,
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

        # if update is set to False saves the new job details to the database.
        # if update is set to True overide an existing job row with the new
        # job details.
        if not kwargs['update']:
            return record.save()
        return self.update_job(kwargs['row_id'], record)

    def get_all_jobs(self, sort_by=-1):
        """get_by_user_id(int) -> return(list[objID(..),..,objID(..)])

        Returns a list all the jobs worked by the users in descending
        order (default mode).

        :parameters
           - sort_by : Takes two parameters in the form of either (-1 or 1).
                      -1: Sorts in descending order .e.g. 10, 9, 8, 7,....,1.
                       1: Sorts in ascending order  .e.g. 1,2,3,4 ,..., 10.
        """
        return Record.find_by_user_id(self.id, sort_by)
        _id=None,

    def get_job_by_row_id(self, row_id):
        """get_job_by_row_id(None) -> return(list[obj(..)])

        Queries the records for a particular job object based on its
        row id. Returns a list containing a single job object with that
        row ID.

        :parameters
           - row_id  : Searches the database using a specific
                       row id and returns a job object.
        """
        return Record.find_by_row_id(row_id, self.id)

    def get_job_by_year(self, year):
        """get_job_by_year(str) -> returns(list[obj(..), .., obj(..)] or None))

        Returns a list of job objects worked in that year or None if
        not found.
        """
        return Record.find_by_year(year, self.id)

    def get_job_by_date(self, date):
        """get_job_by_date(str) -> return(list[obj(..),..,obj(..)] or none)

        Queries the records by a single date and returns a list of job object
        based on that specific date. Returns None if not found.

        :parameters
           - date : Returns all the jobs worked for
                    that specific date.
        """
        return Record.find_by_date(date, self.id)

    def get_job_by_day(self, day):
        """get_by_date_and_day(str) -> return(str)

        Queries the records by a specific day. Returns a list of job objects
        containing all jobs found for that day and none otherwise.

        :parameters
           - day : Searches the records for all jobs worked on that specific day.
        """
        return Record.find_by_day(day, self.id)

    def get_job_by_date_range(self, date_one, date_two):
        """get_by_date_range(str, str) -> return(list[obj(..),..,obj(..)] or none)

        Queries the records for the days worked between two dates. This includes
        both the starting and ending date. Returns a list of job objects if the
        parameters match and None otherwise.

        :parameters
            - date_one: The starting date.
            - date_two: The end date.
        """
        return Record.find_by_date_range(date_one, date_two, self.id)

    def get_job_by_month_range(self, month_one, month_two):
        """get_job_by_month_range(str, str) -> return(list[obj(..),..,obj(..)] or none)

        Returns a list containing all jobs worked between two given months.
        The jobs include the ones worked for the starting month (month_one)
        and the ones for the ending month (month_two). None is returned if
        no jobs are found.

        :parameters
            - month_one: The first month to query by.
            - month_two: The second month to query by.
         """
        return Record.find_by_month_range(month_one, month_two, self.id)

    def get_job_by_month(self, month):
        """get_by_month(str) -> return(list[obj(..),..,obj(..)] or none)

        Queries the records for all jobs worked for a specific month.
        Returns a list of job objects containing all jobs worked for that month
        and None otherwise.

        :parameters
           - month  : The month to query by.
        """
        return Record.find_by_month(month, self.id)

    def get_job_by_start_time(self, start_time):
        """get_job_by_start_time(str) -> return(list[obj(..),..,obj(..)] or none)

        Queries the records based on the time the job starts and returns a list
        of job objects that match the parameter or None otherwise.

        :parameters
           - start_time: The start time to query by. Time must be entered as a
                         string in the form of hh:mm.

        >>> get_by_start_time('11:00')
        objectID(..)
        >>> get_by_start_time('12:00')
        None
        """
        return Record.find_by_start_time(start_time, self.id)

    def get_job_by_finish_time(self, finish_time):
        """get_by_time(str) -> return(list[obj(..),..,obj(..)] or none)

        Queries the records based on the time the job finishes.Returns a list of
        job objects that match the given parameter. None is returned if the
        parameters are not matched.

        :parameters
           - finish_time: The ending time for the job.
                          The finish time is in the form of hh:mm.

        >>> get_by_finish_time('11:00')
        objectID(..)
        >>> get_by_finish_time('12:00')
        None
        """
        return Record.find_by_finish_time(finish_time, self.id)

    def get_by_job_hours(self, hours):
        """get_by_hours(float) -> return(list[obj(..),..,obj(..)] or none)

        Queries the records based on the number of hours worked for a job.
        Returns a list of job objects that match the given parameter.
        Return None if not found.

        :parameters
           - hours: Queries by hours. Hours must be entered as float.
                    For example 2 hrs and 10 mins must be entered as 2.10.

        >>> get_by_hours(2.10)
        [objectID(...)]
        """
        return Record.find_by_hours_worked(hours, self.id)

    def get_by_job_title(self, job_title):
        """get_by_job_title(str) -> return(list[obj(..),..,obj(..)] or none)

        Queries the records by the job title and returns a list of job objects
        that match the parameter job title. Returns None if not matched.

        :parameters
           - job_title : The job title to query by.
        """
        return Record.find_by_job_title(job_title, self.id)

    def get_by_daily_rate(self, daily_rate):
        """get_by_daily_rate(float) -> return(list[obj(..),..,obj(..)] or none)

        Queries the records by the daily rate. Returns a list of job objects
        if found or None otherwise.

        :parameters
          - daily_rate: The daily rate (float) to query by.
        """
        return Record.find_by_daily_rate(float(daily_rate), user_id=self.id)

    def get_by_job_location(self, loc):
        """get_by_location(str) -> return(list[obj(..),..,obj(..)] or none)

        Queries by job location and returns a list of job object
        if found or None otherwise.

        :parameters
            - loc: The location of job to query by.
        """
        return Record.find_by_location(loc, self.id)

    def to_json(self):
        """return all jobs belonging to user in json format."""
        return Record.get_records_in_json(self.id)

    def delete_job(self, row_id):
        """delete_job_row(str) -> return('')
        Deletes a job row from the database using the row id.

        :parameters
           - row_id: The job row to delete.
        """
        Record.delete_row(row_id, self.id)
        return ''

    def update_job(self, row_id, form):
        """update_job_row(str, obj) -> return(None)

        Updates a particular job row with new job information.
        Returns None.

        :parameters
           - row_id: The row id assigin to a job within a database.
           - form  : Form contains the new job information which would be used
                     to overide the information in the old row id with the
                     information from the new the form object.
        """
        return Record.update(row_id, form)

    def get_job_by_confirmation(self, confirmation):
        """get_job_by_confirmation(str) -> return(list[obj(..),..,obj(..)])

        Depending on the confirmation given by the user returns
        a list of job object that are either confirmed or not confirmed.

        :parameters
           - confirmation : either 'yes' or 'no'.

        >>> get_by_confirmation('yes')
        objectID(...)
        >>> get_by_confirmation('no')
        """
        return Record.find_by_confirmation(self.id, confirmation)

    def send_jobs_by_email(self):
        """Sends the latest jobs by email. That is jobs that are starting on
        the current working day.
        """
        pass

    def __repr__(self):
        return '{}'.format(self.full_name)
