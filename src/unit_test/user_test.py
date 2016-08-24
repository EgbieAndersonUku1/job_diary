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
total_hours =  '9'
month       = '08'


user  = User(name, start_date, end_date, day, id)
def is_data_correct(obj):
    count = 0
    def is_true(value1, value2):
        if value1 == value2.title():
            global count
            count += 1

    if not obj:
        return False

    obj = obj[0]
    print '[+] Testing job title parameter', is_true(obj.job_title, job_title.title())
    print '[+] Testing job description parameter', is_true(obj.descr,job_title.title())
    print '[+] Testing daily rate parameter', is_true(obj.daily_rate, daily_rate)
    print '[+] Testing day parameter', is_true(obj.start_time, start_time)
    print '[+] Testing job_title parameter', is_true(obj.finish_time, finish_time)
    print '[+] Testing description parameter', is_true(obj.hourly_rate, hourly_rate)
    print '[+] Testing location parameter', is_true(obj.total_hours, total_hours)
    return count

def does_obj_exists(func, arg):
    rec_obj = func(arg)[0]
    if rec_obj:
        print 'Objection successful retreived data obj'
        sleep(0.05)
        print 'Checking whether the data matches the given parameters'
        sleep(0.05)

def run_test():

    count = 0

    # get the job title
    print 'Test user model to see whether data is successful adds and retreives..'
    print 'Running a series of test to ..'

    print '[+] Add a series of jobs details to the user object '
    print """ [+] {}
              [+] {}
              [+] {}
              [+] {}
              [+] {}
              [+] {}
              [+] {}
              [+] {}\n\n

    """.format(name, start_date, end_date,day,job_title, descr, loc, start_time, finish_time, hourly_rate)

    user.add_job_details(job_title, descr, loc, start_time, finish_time, hourly_rate)
    print '[+] Successfully added details to user model'
    print '[+] Running a series of 7 tests...'

    values = ["start_date ",  "end_date",  "start_date", "day", "loc",
             "start_time",  "finish_time", "hourly_rate", "total_hours", "month" ]

    methods = []
    # ??? NOT WORKING PROPERLY BECAUSE NOT ALL METHODS FOR THE RECORDS ARE PASSED
    # ADD CODE THAT CONTAINS A LIST OF METHODS FOR THE RECORDS THAT PASSES THE ACTUAL METHODS TO THE FUNCTION
    # THIS WILL PROPERLY BE A FOR LOOP HERE
    # HOW TO DO THIS ????

    tests = 0
    for number, job_attribute in  enumerate(values):
        print '[*] Running test number ({}) retreiving value by : ({}) '.format(number+1, job_attribute.upper())
        sleep(1)
        score = is_data_correct(user.get_by_job_title(job_attribute))
        if score == len(values):
            print '[+] Successfully passed all test attributes\n'
            tests += 1
        else:
            print '[-] One or more values of the test did not pass\n'


    if tests == len(values):
        print 'SUCCESSFUL PASSED ALL TESTS : '
    else:
        print '[-] FAILED TESTS -> NUMBER OF TEST FAILED ; {} '.format(tests)
