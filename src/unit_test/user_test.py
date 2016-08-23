# TEST WHETHER THE APPLICATION IS WORKING PROPERLY
import os
from src.models.records import Records
from src.models.users import User
from src.users.models import Login, Registration
from time import sleep

# TEST WHETHER THE USER MODEL IS WORKING CORRECTLY
name       = 'Egbie Uku'
start_date = '23/08/2016'
end_date   = start_date
day        = 'Tuesday'
id         =  None
job_title  = 'bartender'
descr      = 'working as the president for a day'
loc        = 'London'
start_time = '10:00'
finish_time = '21:00'
hourly_rate = '150.00'

user  = User(name, start_date, end_date, day, id)


def run_test():

    count = 0

    # get the job title
    print 'Test user model to see whether data is successful adds and retreives..'
    print 'Running a series of test to ..'

    print '[+] Add a series of jobs details to the user object '
    user.add_job_details(job_title, descr, loc, start_time, finish_time, hourly_rate)
    print '[+] Successfully added details to user model'

    print '\nChecking to see whether job can be retreived by title.'
    print '[+] Retreiving date by date...'
    sleep(0.05)
    rec_obj = user.get_by_job_title(job_title)[0]
    print rec_obj.job_title
    print job_title.title()

    print 'IS SUCCESSFUL : ' + str(rec_obj.job_title).strip() == job_title.title()
    count += 1

    # ADD TEST TO RETREIVE MONTH

    # ADD TEST TO RETREIVE BY day

    # ADD TEST TO RETREIVE hours

    # ADD TEST TO RETREIVE MONTH

    # ADD TEST TO RETREIVE

    # ADD TEST TO RETREIVE

    # ADD TEST TO RETREIVE  
