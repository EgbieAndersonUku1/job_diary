##################################################################
# Author ; Egbie
# Unit Test
# The unit tests whether the connection between the python
# program and the database is active. It does so by testing
# whether data can be added to the database, whether it can can
# be deleted and finally modified.
#
# TO RUN THE TEST
#  >>> python run.py shell
#  This will activate a shell with all the data loaded into memory.
#  If this command is not run the python program returns an importError
#  because the file cannot be find. Next run.
#
# >>> from src.Users.Unit_tests.database_test import DataBaseTest
# >>> db = DataBaseTest()
# The second command will initialized the database.
##################################################################

from src.Users.user import User
from src.Users.Models.Databases.database import DataBase
from src.Users.Jobs.job_helper import get_hours_worked, get_daily_rate
from src.utilities.converter import time_to_str, month_to_str, hours_to_units
from time import sleep
from datetime import datetime
from collections import OrderedDict
from sys import exit

DATABASE_INITIALIZE = False

def initialize_database():
    """initialize the database"""
    print'[*] initializing the database please wait...'
    DataBase.initialize()
    print'[+] Database initialized.'

class DataBaseTest(User):
    """Test whether the data can effectively be added/deleted/modified from
    the database
    """
    def __init__(self, username='Egbie', start_date='2016-12-26', end_date='2016-12-26',
                day='Monday', _id='1234'):
                # check whether the database has been initialized.
                global DATABASE_INITIALIZE
                if not DATABASE_INITIALIZE:
                    initialize_database()
                    DATABASE_INITIALIZE = True

                User.__init__(self, username, start_date, end_date, day, _id=_id)
                year, month, day = start_date.split('-')
                self.user_id = _id
                self.job_title = 'King'
                self.descr = 'Running Asgardian for a day'
                self.loc  = 'Asgard'
                self.start_time = '10:00'
                self.finish_time = '21:00'
                self.hourly_rate = 15000.25
                self.is_shift_confirmed = True
                self.worked_job = 'No'
                self.username = username
                self.start_date = start_date
                self.end_date = end_date
                self.row_id = None
                self.year = int(year)
                self.month = month_to_str(str(month))
                self.day = day
                self.hours = get_hours_worked(self.start_date,
                                              self.start_time,
                                              self.end_date,
                                              self.finish_time)
                self.units = hours_to_units(self.hours) # change hrs to units
                self.daily_rate = get_daily_rate(self.units, self.hourly_rate)
                self.errors = OrderedDict()

    def set_worked_job(self, status):
        """change the status of the worked jobs"""
        self.worked_job = status.title()

    def set_job_title(self, role):
        """change the title of the job"""
        self.job_title = role

    def set_job_descr(self, descr):
        """change the description for the job"""
        self.descr = descr

    def set_loc(self, loc):
        """change the location of the job"""
        self.loc = loc

    def set_start_time(self, start_time):
        """change the start time of the job"""
        self.start_time = start_time

    def set_finish_time(self, finish_time):
        """change the finish time for the job"""
        self.finish_time = finish_time

    def set_hourly_rate(self, hourly_rate):
        """set the hourly rate"""
        self.hourly_rate = hourly_rate

    def set_shift_confirmation(self, confirmation):
        """set the confirmation for the shift"""
        self.is_shift_confirmed = confirmation

    def set_worked_job(self, status):
        """set the whether job is worked or not worked"""
        self.worked_job = status

    def set_username(self, username):
        """set the username"""
        self.username = username

    def set_start_date(self, date):
        """set the start date for the job"""
        self.start_date = date

    def set_end_date(self, end_date):
        """set the end date for the job"""
        self.end_date = end_date

    def set_row_id(self, row_id):
        """set the row id for the job"""
        self.row_id = row_id

    def set_day(self, day):
        """set the day the job starts"""
        self.day = day

    def reset_values(self):
        """reset the job values"""

        print '\n[+] please wait, reseting cache..'
        self.set_job_title('')
        self.set_job_descr('')
        self.set_loc('')
        self.set_start_time('')
        self.set_finish_time('')
        self.set_hourly_rate('')
        self.set_shift_confirmation(False)
        self.set_start_date('')
        self.set_end_date('')
        print'[+] Done, cache resetted.'

    def _is_job_saved(self, row_id):
        """Check whether the data was successful saved to the database
        Returns True if record find or False otherwise.
        """
        return True if self.get_job_by_row_id(row_id) else False

    def add_job_to_records_test(self):
        """Add job to database test"""
        print("[+] Adding an active job to the database, please wait....")
        row_id = self.add_job_to_records(self.job_title, self.descr, self.loc,
                                         start_time=self.start_time,
                                         finish_time=self.finish_time,
                                         hourly_rate=self.hourly_rate,
                                         is_shift_confirmed=self.is_shift_confirmed,
                                         update=False)

        if self._is_job_saved(row_id): # check if the record was stored in database
            print("[+] Data was successful saved to the database.")
            self.set_row_id(row_id) # replace the old row_id with the latest row_id
            return True
        print("[+] Error, failed to save job to the database.")
        return False

    def _get_jobs(self, status, func, key=None, **kwargs):
        """_get_jobs(str, func) -> return(bool)
        A thin wrapper higher method that retrieved either an active or non active jobs.

        :parameters
           - msg  :  A string that relates information to the user.
           - func :  Takes a method and returns the value.
           - key  :  Used to retreive values from kwargs.
           **kwargs: Information need for the func value.
        """
        print '[*] Attempting to get all {}  for the user, please wait..'.format(status)
        jobs = func() if key == None else func(kwargs[key])
        if jobs:
            print '[+] Successful, retreived all user jobs.'
            return True
        print '[-] Failed to retreive any {} jobs.'.format(status)
        return False

    def get_all_active_jobs_test(self):
        """returned all jobs that user has worked"""
        return self._get_jobs('active jobs', self.get_all_active_jobs)

    def get_all_worked_jobs_test(self):
        """returned all jobs that the user has worked"""
        return self._get_jobs('worked jobs', self.get_all_worked_jobs)

    def get_job_by_name_test(self):
        """return all jobs based on the name"""
        msg = 'jobs based on the name'
        return self._get_jobs(msg, self.get_by_job_title, 'job_title', job_title=self.job_title)

    def get_job_by_loc_test(self):
        """return all jobs based on their location"""
        msg = 'jobs based on the location'
        return self._get_jobs(msg, self.get_by_job_location, 'loc', loc=self.loc)

    def get_job_by_start_time_test(self):
        """return all jobs based on their start time"""
        msg = 'jobs based on their start time'
        return self._get_jobs(msg, self.get_job_by_start_time, 'start_time',
                             start_time=self.start_time)

    def get_job_by_finish_time_test(self):
        """return all jobs based on their finish time"""
        msg = 'jobs based on their finish time'
        return self._get_jobs(msg, self.get_job_by_finish_time, 'finish_time',
                              finish_time=self.finish_time)

    def get_job_by_year_test(self):
        """return all jobs based on the name"""
        msg = 'jobs based on their year'
        return self._get_jobs(msg, self.get_job_by_year, 'year', year=self.year)

    def get_job_by_month_test(self):
        """return all jobs based on the name"""
        msg = 'jobs based on their month'
        return self._get_jobs(msg, self.get_job_by_month, 'month',
                              month=self.month[:3].title())

    def get_job_by_day_test(self):
        """return all jobs based on the name"""
        msg = 'jobs based on the day'
        return self._get_jobs(msg, self.get_job_by_day, 'day', day=self.day)

    def get_job_by_hours_test(self):
        """return all jobs based on the name"""
        msg = 'jobs based on the hours worked'
        return self._get_jobs(msg, self.get_by_job_hours, 'total_hours',
                              total_hours=self.units)

    def get_job_by_daily_rate_test(self):
        """return all jobs based on the name"""
        msg = 'jobs based on their daily rate'
        return self._get_jobs(msg, self.get_by_daily_rate, 'daily_rate',
                              daily_rate=self.daily_rate)

    def get_job_by_start_date_test(self):
        """return all jobs based on the name"""
        msg = 'jobs based on the start date'
        return self._get_jobs(msg, self.get_job_by_date, 'date', date=self.start_date)

    def get_job_by_row_id_test(self):
        """return all jobs based on the name"""
        msg = 'jobs based on the row id'
        return self._get_jobs(msg, self.get_job_by_row_id, 'row_id', row_id=self.row_id)

    def get_job_by_user_id_test(self):
        """return all jobs based on the name"""
        msg = 'jobs based on the user id'
        return self._get_jobs(msg, self.get_all_jobs)

    def delete_job_test(self):
        """check if the jobs can be deleted from the database"""

        print '\n[+] Attempting to delete job from database, please wait...'
        self.delete_job(self.row_id.replace('#', ''))
        print '[+] Done, checking to see if job was deleted, please wait..'
        if self.get_job_by_row_id(self.row_id):
            print '[-] Failed to delete job from the database'
            return False
        print '[+] Successful deleted job from the database.'
        return True

    def update_job_status_test(self, status, row_id=None):
        """Allows the status of the job to be updated"""

        print '[*] Please wait, attempting to change the job status..'
        if not row_id:
            print '[+] Failed to change because the row id is None.'
            return False
        elif row_id:
            self.set_row_id(row_id)

        self.update_job_status(self.row_id, status)
        if status.title() == 'Yes':
            value = self.get_all_worked_jobs()
        else:
            value = self.get_all_active_jobs()
        if value:
            print '[-] Successful changed the job status to: "{}"'.format(status).title()
            return True
        print '[+] Failed to change job status!!'
        return False

    def _is_valued_changed(self, obj, obj2):
        errors  = {}

        values = ["end_date", "descr", "is_shift_confirmed",
                  "finish_time","start_time","month", "total_hours",
                  "daily_rate", "year", "date", "hourly_rate","job_title"]

        for value in values:
            if obj[value] == obj2[value]:
                errors[value] = '[-] Failed to update the [{}] value..'.format(value)
        return errors

    def modified_data_test(self):
        """test whether in database can be modified"""

        assert self.row_id, 'The row ID cannot be an empty string or False.'
        old_record = self.get_job_by_row_id(self.row_id)      # returned as object
        old_rec = DataBase.find_one('jobs_details', {'row_id': self.row_id}) # returns json instead of object
        count = 0

        # The new data that would be used to modified the existing the data
        print '[+] Creating new job attributes that would be used as new job values.'
        self.set_job_title('Programmer')
        self.set_job_descr('Working as a programmer')
        self.set_loc('The tardis')
        self.set_start_time('06:00')
        self.set_finish_time('15:00')
        self.set_hourly_rate(19.0)
        self.set_shift_confirmation(False)
        self.set_start_date('2017-02-27')
        self.set_end_date('2017-05-16')

        new_row_id = self.add_job_to_records(self.job_title,
                                             self.descr, self.loc,
                                             start_time=self.start_time,
                                             finish_time=self.finish_time,
                                             hourly_rate=self.hourly_rate,
                                             is_shift_confirmed=self.is_shift_confirmed,
                                             start_date=self.start_date,
                                             end_date=self.end_date,
                                             worked_job=self.worked_job,
                                             row_id=self.row_id,
                                             update=True) # returns a new row id

        self.set_row_id(new_row_id)
        new_record = self.get_job_by_row_id(self.row_id) # get the new updated records
        new_rec = DataBase.find_one('jobs_details', {'row_id': self.row_id}) # returned as json
        return self._is_valued_changed(old_rec, new_rec)

    def _is_test_passed(self, result, failed, successful, errors, key, error_msg):
        """Checks whether the test has been passed"""

        sleep(0.5)
        if result:
            successful.append(1)
            errors[key] = '[+] Successful passed.'
            return
        errors[key] = error_msg
        failed.append(1)

    def _get_summary(self, errors, tests, successful_test, failed_test):
        """returns a summary of the entire test"""
        print '\n\n\n'
        print "=" *40
        print "[+] Date test was run  on : {}".format(datetime.utcnow())
        print "\n"
        print "[+] The total test run was {}".format(tests)
        print "[+] The number of test passed was : {}".format(sum(successful_test))
        print "[+] The number of test failed was : {}".format(sum(failed_test))

        if not errors:
            print "[+] All methods are within working parameters"
        else:
            print '\n[-] printing the summary of the test ...\n'
            for key in self.errors:
                print "{} : {}".format(key, self.errors[key])
        print "="*40

    def _get_error_report(self, errors):
        """generate an error report"""
        print '\n\n\n Report for job that did not update..'
        for key in errors:
            print "[-] {} :: {}".format(key.title(), errors[key])
        print "\n\n"

    def run_tests(self):
        """run the test to determine if access to the database is okay"""
        NUM_OF_TESTS = 18
        failed_test, successful_test = [], []

        print '##################### Preparing tests...#####################'.center(40)
        print '\n\n[+] Test 1: Setting up fake data to be used for the database..'
        print '[+] Adding data to the database, please wait'
        print '[+] Checking if the data was successful saved to database'
        test_one  = 'Test 1'
        error_msg = 'Error : Failed to save data to database'
        self._is_test_passed(self.add_job_to_records_test(), failed_test,
                             successful_test, self.errors,test_one,
                             error_msg)

        print '\n[+] Test 2:'
        print '[+] Checking to see if active (jobs not worked) can be retreived..'
        test_two  = 'Test 2 :'
        error_msg = 'Error : Failed to retreive active jobs.'
        self._is_test_passed(self.get_all_active_jobs_test(), failed_test,
                             successful_test, self.errors, test_two,
                             error_msg)

        print '\n[+] Test 3:'
        print '[+] Check to see if the job status can be changed.'
        test_three  = 'Test 3 :'
        error_msg = 'Error : Failed to change job status.'
        self._is_test_passed(self.update_job_status_test('yes', self.row_id),
                             failed_test, successful_test, self.errors,
                             test_three, error_msg)

        print '\n[+] Test 4:'
        print '[+] Checking to see if non-active jobs (jobs worked) can be retreived..'
        test_four  = 'Test 4 :'
        error_msg = 'Error : Failed to retreive worked jobs.'
        self._is_test_passed(self.get_all_worked_jobs_test(), failed_test,
                             successful_test, self.errors,
                             test_four, error_msg)

        print '\n[+] Test 5:'
        print '[+] Checking to see jobs can retreived by name..'
        test_five  = 'Test 5 :'
        error_msg = 'Error : Failed to retreive jobs based on their name'
        self._is_test_passed(self.get_job_by_name_test(), failed_test,
                             successful_test, self.errors, test_five,
                             error_msg)

        print '\n[+] Test 6:'
        print '[+] Checking to see if jobs can be retreived by location..'
        test_six  = 'Test 6 :'
        error_msg = 'Error : Failed to retreive data by location'
        self._is_test_passed(self.get_job_by_loc_test(), failed_test,
                             successful_test, self.errors, test_six,
                             error_msg)

        print '\n[+] Test 7:'
        print '[+] Checking to see if jobs can be retreived by start time..'
        test_seven  = 'Test 7 :'
        error_msg = 'Error : Failed to retreive job by start time'
        self._is_test_passed(self.get_job_by_start_time_test(), failed_test,
                            successful_test, self.errors,
                            test_seven, error_msg=error_msg)

        print '\n[+] Test 8:'
        print '[+] Checking to see if jobs can be retreived by finish time..'
        test_eight  = 'Test 8 :'
        error_msg = 'Error : Failed to retreive jobs by finish time.'
        self._is_test_passed(self.get_job_by_finish_time_test(), failed_test,
                             successful_test, self.errors,
                             test_eight, error_msg)

        print '\n[+] Test 9:'
        print '[+] Checking to see if jobs can be retreived by year..'
        test_nine  = 'Test 9 :'
        error_msg = 'Error : Failed to retreive jobs by the year worked.'
        self._is_test_passed(self.get_job_by_year_test(), failed_test,
                             successful_test, self.errors,
                             test_nine, error_msg)

        print '\n[+] Test 10:'
        print '[+] Checking to see if jobs can be retreived by month..'
        test_ten  = 'Test 10 :'
        error_msg = 'Error : Failed to retreive jobs based on the month worked'
        self._is_test_passed(self.get_job_by_month_test(), failed_test,
                             successful_test, self.errors,
                             test_ten, error_msg)

        print '\n[+] Test 11:'
        print '[+] Checking to see if jobs can be retreived by day..'
        test_eleven  = 'Test 11 :'
        error_msg = 'Error : Failed to retreive jobs by days worked'
        self._is_test_passed(self.get_job_by_day_test(), failed_test,
                             successful_test, self.errors,
                             test_eleven, error_msg)

        print '\n[+] Test 12:'
        print '[+] Checking to see if jobs can be retreived by hours..'
        test_twelve  = 'Test 12 :'
        error_msg = 'Error : Failed to retreive job by hours worked'
        self._is_test_passed(self.get_job_by_hours_test(), failed_test,
                            successful_test, self.errors,
                            test_twelve, error_msg)

        print '\n[+] Test 13:'
        print '[+] Checking to see if jobs can be retreived by the daily rate..'
        test_thirteen  = 'Test 13 :'
        error_msg = 'Error : Failed to retreive job by the daily rate'
        self._is_test_passed(self.get_job_by_daily_rate_test(), failed_test,
                             successful_test, self.errors,
                             test_thirteen, error_msg)

        print '\n[+] Test 14:'
        print '[+] Checking to see if jobs can be retreived by start date..'
        test_fourteen  = 'Test 14 :'
        error_msg = 'Error : Failed to to retreive job by the start date'
        self._is_test_passed(self.get_job_by_start_date_test(), failed_test,
                             successful_test, self.errors,
                             test_fourteen, error_msg)

        print '\n[+] Test 15:'
        print '[+] Checking to see if jobs can be retreived by row id..'
        test_fifteen  = 'Test 15 :'
        error_msg = 'Error : Failed to retreive job based on the row id'
        self._is_test_passed(self.get_job_by_row_id_test(), failed_test,
                             successful_test, self.errors,
                             test_fifteen, error_msg)

        print '\n[+] Test 16:'
        print '[+] Checking to see if jobs can be retreived by on user ID..'
        test_sixteen  = 'Test 16 :'
        error_msg = 'Error : Failed to to retreive jobs based on the user id'
        self._is_test_passed(self.get_job_by_user_id_test(), failed_test,
                             successful_test, self.errors, test_sixteen, error_msg)

        print '\n[+] Test 17'
        print '[+] Checking to see if job within the database can be modified...'
        test_seventeen = 'Test 17 :'
        errors = self.modified_data_test()
        passed_test = False
        if not errors:
            print '[+] Successful modified jobs within the database.'
            passed_test = True
        else:
            print '\n[+] Test 17 failed generating error report..'
            self._get_error_report(errors)

        error_msg = 'Error : Failed to modified jobs in the database'
        self._is_test_passed(passed_test, failed_test, successful_test,
                             self.errors,test_seventeen, error_msg)

        print '\n[+] Test 18:'
        print '[+] Checking to see if jobs can be deleted from database..'
        test_eighteen  = 'Test 18 :'
        error_msg = 'Error : Failed to to delete job from the database.'
        self._is_test_passed(self.delete_job_test(), failed_test, successful_test,
                             self.errors,test_eighteen, error_msg)

        self._get_summary(self.errors, NUM_OF_TESTS, successful_test, failed_test)
        self.reset_values()
        print'[+] Test will exiting in 5 seconds...\n'
        sleep(5)
        print'##################### Test complete have a nice day #####################'.center(40)
