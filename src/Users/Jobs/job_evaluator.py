# -*- coding: utf-8 -*-

##############################################################################
# Author : Egbie
#
# THE EVALUATOR SOLE PROCESS IS TO DETERMINE HOW THE USERS JOB SHOULD BE STORED
# IN THE DATABASE WHETHER THAT IS AS A JOB THAT HAS ALREADY BEEN WORKED,
# A JOB THAT IS YET TO BE WORKED OR WHETHER IT SHOULD BE DELETED.
#
#
# IT DOES THIS IN STAGES. THE FIRST STAGE IS TO DETERME WHETHER THE JOB
# HAS ALREADY HAPPENED (PAST) IN THAT CASE IT KEEP IT AS A PART OF THE USER'S
# JOB HISTORY ONLY IT'S CONFIRMED, WHETHER THE JOB IS OCCURRING IN
# THE PRESENT OR IN THE FUTURE.
#
# THE NEXT STAGE IS TO DETERMINE THE CONFIRMATION OF THE JOB AND THEN FLAG
# IT AS THE FOLLOWING.
#
#  CONFIRMED   : THE JOB HAS BEEN CONFIRMED AND IS SCHEDULED TO HAPPENED.
#  UNCONFIRMED : THE JOB WAS NOT CONFIRMED AND THEREFORE IS NOT HAPPENING.
#  NOT YET     : THE USER IS STILL WAITING FOR CONFIRMATION OF THE JOB.
#
#
# IF THE JOB IS SCHEDULED TO HAPPEN EITHER IN THE PRESENT OR IN THE FUTURE BUT
# HAS NOT YET BEEN CONFIRMED IT FLAGGED AS 'NOT YET' AND STORED IN THE DATABASE
# AND ONCE CONFIRMED IT IS THEN FLAGGED AS 'CONFIRMED'.
#
# IF THE JOB IS FLAGGED AS 'NOT YET' AND IS NOT CONFIRMED BY
# THE TIME THE JOB SCHEDULED START TIME ARRIVES, IT IS THEN FLAGGED AS
# UNCONFIRMED WHICH IS THEN REMOVED FROM DATABASE.
#
# IF THE JOB DIARY IS USED AS A DIARY A WAY TO KEEP RECORD OF A JOBS
# THAT HAS ALREADY HAPPENED (PAST). IT MUST BE ENTERED AS 'YES' IN THE
# 'SHIFT CONFIRMED' FIELD LOCATED IN ENTRY JOB PAGE. OTHERWISE EVALUATOR WILL FLAG
# THE JOB AS 'UNCONFIRMED' AND WILL NOT EVEN ADD IT TO THE DATABASE.
# THIS IS BECAUSE EVALUATOR KNOWS YOU ARE ADDING A JOB THAT IS IN THE PAST
# AND NOT ONE THAT'S SCHEDULED TO HAPPEN EITHER IN THE PRESENT OR IN THE FUTURE
# AND SO DEEMS IT AS UNCONFIRMED FROM THE START. AS SINCE IT IS IN THE PAST
# IT IS NOT EVEN ADDED TO THE DATABASE.

# TO PREVENT THIS FROM HAPPENING THE JOB MUST BE ENTERED AS CONFIRMED
# IN THE GUI PAGE, THIS WAY EVALUATOR KNOWS YOU STORING IT AS A RECORD
# AND THAT THE JOB IS NOT HAPPENING SO THERES NO NEED TO WAIT FOR A
# CONFIRMATION.
#
##############################################################################

from flask import session
from src.Users.user import User
from src.utilities.common import create_flash_msg
from src.Users.Jobs.job_helper import (is_shift_over,
                                       is_job_in_past_present_or_future,
                                       is_shift_confirmed,
                                       is_shift_now)

class Evaluator(object):
    """Evaluator:(Class)
    Evalulates the user's job details and stores it in the database
    accordingly.
    """
    job_confirmed = ''

    @classmethod
    def set_job_confirmation(cls, job=None, confirmation='No', job_confirmed='unconfirmed'):
        """set_job_confirmation(obj, str, str) -> returns(None)

        Allows the job confirmation to be set.

        :parameters
           - job : The job object. Default mode(None)
           - confirmation: 'Yes' or 'No' used to set the
                           whether the job was confirmed.
           - job_confirmed: Takes either 'unconfirmed', 'confirmed' or 'not yet',
                            and uses it to flag the job.

                            confirmed: This tells the database to store it
                                       as a job that is already confirmed.
                            not yet: Tells the database to flag it as a job
                                     that is still waiting to be confirmed.
                            unconfirmed: Flags the job as a job that would be
                                         deleted.
        """
        if job:
            job.is_shift_confirmed = confirmation
        cls.job_confirmed = job_confirmed

    @classmethod
    def set_worked_job(cls, job, status):
        """Sets the job as either worked or not worked

        :parameters
           - job : a job object.
           - status: string either yes or no. Set the job
                     to yes if worked and no if not.
        """
        job.worked_job = status

    @classmethod
    def update_job_status_in_db(cls, user, row_id, worked_job, reset=False):
        """updates the status of the job in the database"""
        if reset:
            user.update_job_status(row_id, 'No')
            return
        user.update_job_status(row_id, worked_job)

    @classmethod
    def _save(cls, user, job, row_id=None, update=False):
        """A wrapper function which saves the data to database.
        If row_id is true and update is set to true
        updates a previous row with the new data.

        Returns a row id.
        """
        if update:
            cls.update_job_status_in_db(user, row_id, job.worked_job)
        return user.add_job_to_records(job.job_title,
                                       job.description,
                                       job.location,
                                       worked_job=job.worked_job,
                                       start_time=job.start_time,
                                       finish_time=job.finish_time,
                                       hourly_rate=job.rate,
                                       is_shift_confirmed=job.is_shift_confirmed,
                                       update=update, row_id=row_id)

    @classmethod
    def _save_to_database(cls, user, job, row_id=None, update=False):
        """Saves the user's job details to the database."""

        if cls.job_confirmed == 'unconfirmed':
            create_flash_msg('Job was deleted because it was not confirmed.')
            user.delete_job(row_id[1:])
            return cls.job_confirmed, None
        elif cls.job_confirmed == 'not yet':
            create_flash_msg("""The job needs to be confirmed before the
                             start of the job date or it wiil be deleted
                             automatically.""")
            row_id = cls._save(user, job, row_id, update) # save to db
        elif cls.job_confirmed == 'confirmed':
            create_flash_msg('The job has been added to database.')
            row_id = cls._save(user, job, row_id, update) # save to db
        return cls.job_confirmed, row_id

    @classmethod
    def _evaluate(cls, job_status, confirmed, job):
        """evaluates the details of the job provided by the user"""

        if job_status == 'past' and confirmed:
            cls.set_worked_job(job, 'Yes')
            cls.set_job_confirmation(job, 'yes', 'confirmed')
        elif job_status == 'past' and not confirmed:
            cls.set_job_confirmation(job, job_confirmed='unconfirmed')
        elif job_status  == 'present':
            # The shift has started but it was never confirmed
            # which means the user never worked the shift/job
            if not confirmed and is_shift_now(job):
                cls.set_job_confirmation(job_confirmed='unconfirmed')

            # The job has not been confirmed yet. But since
            # the job is in the present it is flagged as
            # not yet started. The means the user has
            # till the start of job/shift in order to confirm.
            elif not confirmed and not is_shift_now(job):
                cls.set_job_confirmation(job_confirmed='not yet')

            # user current working the shift
            elif confirmed and is_shift_now(job):
                cls.set_job_confirmation(job, 'yes','confirmed')

            # confirmed but the shift has not yet started.
            elif confirmed and not is_shift_now(job):
                cls.set_job_confirmation(job_confirmed='confirmed')

            # the shift/job was worked by the user.
            elif confirmed and is_shift_over(job):
                cls.set_worked_job(job, 'Yes')
                cls.set_job_confirmation(job, 'yes', 'confirmed')

        elif job_status == 'future':
            if not confirmed:
                cls.set_job_confirmation(job_confirmed='not yet')
            elif confirmed:
                cls.set_job_confirmation(job, 'yes', 'confirmed')
        return job

    @classmethod
    def evaluate_and_save(cls, job, curr_date, row_id=None, update=False):
        """process_form(str, str, str) -> return(tuple)

        Processes the form and adds the user job details to
        the database.
        """
        when_job  = is_job_in_past_present_or_future(job, curr_date)
        confirmed = is_shift_confirmed(job)
        user = User(session['username'], job.start_date,
                     job.end_date, job.day, _id=session['user_id'])

        if update:
            cls.update_job_status_in_db(user, row_id, job, True) # reset the worked job to No
            updated_job = cls. _evaluate(when_job, confirmed, job)
            create_flash_msg('A job was updated.')
            return cls._save_to_database(user, updated_job, row_id, True)

        job = cls._evaluate(when_job, confirmed, job)
        return cls._save_to_database(user, job)
