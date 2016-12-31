##############################################################################
# Author : Egbie
##############################################################################

from flask import session
from src.Users.user import User
from src.utilities.common import create_flash_msg
from src.Users.Jobs.job_helper import (is_shift_over,
                                       is_job_in_past_present_or_future,
                                       is_shift_confirmed,
                                       is_shift_now)

class Evaluator(object):

    status = 'unconfirmed'


    @classmethod
    def set_confirmation(cls, status):
        cls.status = status

    @classmethod
    def _save_to_db(cls, user, job, row_id=None, update=False):

        """The save function saves the data to database.
        If row_id is not false and update is equal to true
        updates a previous row with the
        new data.

        Returns a row id.
        """
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
    def _update_job_status(cls, user, status, update, job=None,
                           row_id=None, confirmed='confirmed'):

        cls.set_confirmation(confirmed)
        if update:
            user.update_job_status(cls._save_to_db(user, job, row_id, True), status) # user has worked the job.
            assert False, 49
        else:
            return cls._save_to_db(user, job)
        return row_id

    @classmethod
    def _evaluate(cls, job_status, confirmed, user, job, row_id=None, update=False):

        if job_status == 'past' and confirmed:
            job.worked_job = 'Yes'
            return cls._update_job_status(user, 'Yes', update, job, row_id)
        elif job_status == 'past' and not confirmed:
            return cls._update_job_status(user, job.worked_job, update, job, row_id)
        elif job_status  == 'present':
            if not confirmed and is_shift_now(job):
                return None  # shift started but was unconfirmed

            # The shift has not yet started but is not confirmed yet
            elif not confirmed and not is_shift_now(job):
                cls.set_confirmation('not yet')
                return cls._save_to_db(user, job)
            elif confirmed  and is_shift_now(job): # user current working the shift
                cls.set_confirmation('confirmed')
                return cls._save_to_db(user, job),
            elif confirmed and not is_shift_now(job):
                cls.set_confirmation('not yet')
                return cls._save_to_db(user)
            elif confirmed and is_shift_over(job): # the current shift is now over
                return cls._update_job_status(user, 'Yes', update, job, row_id, True)
        elif job_status == 'future':
            return cls._save_to_db(user), 'not yet'
        assert False, job_status

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


        #assert False, when_job
        # job_status, confirmed, user, job,
        if update:
            create_flash_msg('A job was updated.')
            r = cls. _evaluate(when_job, confirmed, user, job, row_id, update=True)
            assert False, r
        return cls._evaluate(when_job, confirmed, user, job), cls.status
