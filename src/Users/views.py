#-*- coding: utf-8 -*-
#####################################################################
# Author = Egbie Uku
#####################################################################

import json
import datetime
import uuid
from src.Users.Validator.date_validator import fix_date
from src.Users.Models.TotalUserMoneys.total_amount import TotalAmount
from src.utilities.converter import time_to_str, units_to_hours, month_to_str
from src.Users.Models.Registrations.registration import Registration
from src.Users.Models.Databases.database import DataBase
from src.Users.decorators import login_required, admin_required
from flask_paginate import Pagination
from src.Users.Validator.secret_question_validator import ValidiateSecretQuestions
from src.Users.Validator.search_form_validator import ValidateSearchForm
from src.Users.Validator.job_entry_validator import ValidateJobDetailsForm
from src.Users.Forms.register_form import RegisterForm
from src.Users.Forms.login_form import LoginForm
from src.Users.Forms.search_form import SearchForm
from src.Users.Forms.forgotten_password_form import ForgottenPasswordForm
from src.Users.Forms.new_password_form import NewPasswordForm
from job_diary import app
from flask import render_template, session, redirect, url_for, request
from registration_and_login_helper import login_user, register_user
from src.utilities.password_hasher import create_passwd_hash
from src.Users.user import User
from src.Users.Jobs.job_evaluator import Evaluator
from src.Users.Models.TotalUserMoneys.total_amount import TotalAmount
from src.Users.Jobs.job_helper import ( get_jobs,
                                        is_shift_now,
                                        is_shift_over,
                                        is_shift_confirmed,
                                        when_is_shift_starting)
date = datetime.datetime.now()
curr_day = datetime.date.today().strftime("%A")
curr_date = "{}-{}-{}".format(date.year, date.month, date.day)
curr_date = fix_date(curr_date)
SEARCH_FORM_JOBS = ''


@app.before_first_request
def initialize():
    """initialize the database"""
    DataBase.initialize()

@app.route('/', methods=('GET', 'POST'))
@app.route('/login', methods=('GET', 'POST'))
def login():
    """Allows the user entry to the login applicaton"""
    form = LoginForm()
    return login_user(form=form,
                      session_name='username',
                      redirect_link='home',
                      template='forms/LoginRegistrationForm/login.html',
                      index='home')

@app.route('/register', methods=('GET', 'POST'))
def user_register():
    """Register the user to the application"""
    form = RegisterForm()
    return register_user(form=form,
                         error='username must be unique',
                         template='forms/LoginRegistrationForm/registration.html',
                         redirect_link='home')

def redirector(row_id, job_status):
    if job_status == 'unconfirmed':
         return redirect(url_for('history'))
    return redirect(url_for('info_page', row_id=row_id))

@app.route('/job/entry/<row_ID>', methods=('GET', 'POST'))
@login_required
def entry_page(row_ID):
    """entry_page(func)
    Retreives and process the users data. Also renders the user data
    from the entry job page.
    """
    start_date, end_date = curr_date, curr_date
    descr   = request.form.get('description', '')
    title   = request.form.get('job_title', '')
    day     = request.form.get('day', curr_day)
    loc     = request.form.get('location', '')
    hourly_rate = request.form.get('hourly_rate', '')
    start_date  = request.form.get('start_date', curr_date)
    end_date    = request.form.get('end_date', curr_date)
    start_hours = request.form.get('start_hours')
    start_mins  = request.form.get('start_mins')
    end_hours   = request.form.get('end_hours')
    end_mins    = request.form.get('end_mins')
    is_shift_confirmed = request.form.get('is_shift_confirmed')

    if request.method == 'GET':
        return render_template('forms/JobEntryForm/job_entry_page.html',
                                start_date=start_date,
                                end_date=end_date,
                                day=day,
                                job_title=title,
                                description=descr,
                                location=loc,
                                start_hours=start_hours,
                                start_mins=start_mins,
                                rate=hourly_rate,
                                end_hours=end_hours,
                                end_mins=end_mins,
                                errors='',
                                success='',
                                is_shift_confirmed=is_shift_confirmed)

    job_form = ValidateJobDetailsForm(title, descr, loc,
                                      hourly_rate, start_date,
                                      end_date, day,
                                      is_shift_confirmed,
                                      start_hours,
                                      start_mins, end_hours,
                                      end_mins)
    success, errors, job = job_form.verify_form()
    if success:
        # row_ID comes from the form so False is expressed as a unicode
        # instead of a boolean. This make the if-condition
        # if row_ID == False or not(row_ID) == False always equals True instead
        # of False.
        # By expressing it as str(row_ID) != 'False' it makes the if-statement
        # False when the string returned is not equal to the string False.
        if str(row_ID) != 'False': # means the row should be updated.
            msg, row_id = Evaluator.evaluate_and_save(job, curr_date, row_ID, True)
            return redirector(row_id, msg)
        else:
            msg, row_id = Evaluator.evaluate_and_save(job,curr_date)
            return redirector(row_id, msg)

    # Render the details already entered by the user.
    return render_template('forms/JobEntryForm/job_entry_page.html',
                           start_date=job.start_date,
                           end_date=job.end_date,
                           job_title=job.job_title,
                           description=job.description,
                           location=job.location,
                           start_hours=job.start_hours,
                           start_mins=job.start_mins,
                           end_hours=job.end_hours,
                           end_mins=job.end_mins,
                           day=job.day,
                           rate=job.rate,
                           errors=errors,
                           is_shift_confirmed=is_shift_confirmed)
@app.route('/logout')
@login_required
def logout():
    """log the user out of the application"""
    if session.get('admin', None):
        session.pop('admin')
    session.pop('username')
    session.pop('user_id')
    session.pop('session_name')
    return (redirect(url_for('login')))

@app.route('/jobs/reset')
@login_required
def reset():
    """reset the value in the form for the application"""
    return redirect(url_for('entry_page', row_ID=False))

@app.route('/deletedpage')
@login_required
def deleted_jobs_page():
    return render_template('forms/deleted/deletedjobs.html')

@app.route('/info/<row_id>')
@login_required
def info_page(row_id):
   """redirects the user to successful page entry after successful input"""
   user = User(session['username'],_id=session['user_id'])
   return render_template('forms/permalinks/perma_table.html', rows=user.get_job_by_row_id(row_id))

def _display(html_link, active=False, permalink_jobs=False):
    """_display(str, str) -> return(value)

    :parameters
        - html_link: The link of the page to render
        - active   : Whether the jobs are active e.g not worked yet.
        - returns  : Render object.

    Renders the jobs worked or not worked along with the hours and total pay.
    """
    jobs, user = get_jobs(active, permalink_jobs,User, session, curr_date)
    return render_template(html_link,
                           jobs=jobs,
                           translate=month_to_str, # total hrs expressed in units e.g 12.75
                           date=curr_date,
                           is_shift_over=is_shift_over,
                           converter=units_to_hours,
                           when_is_shift_starting=when_is_shift_starting,
                           is_shift_now=is_shift_now,
                           is_shift_confirmed=is_shift_confirmed,
                           user=user, len=len, total=TotalAmount)

@app.route('/history/jobs', methods=('GET', 'POST'))
@login_required
def history():
    """renders the entire job history active and none active"""
    return _display('forms/WorkedJobs/jobs_history.html')

@app.route('/active/jobs', methods=('GET', 'POST'))
@login_required
def active_jobs():
    """renders the all jobs that are active (not worked)"""
    return _display('forms/CurrentJobs/current_jobs.html', True)

@app.route('/search/permalinks/jobs')
def perma_link():
    """Displays the jobs retreived from the search function"""
    return _display("forms/permalinks/perma_link.html", permalink_jobs=SEARCH_FORM_JOBS)

@app.route('/job/edit/<value>')
@login_required
def edit(value):
    """Allows the jobs to be edited"""
    user = User(session['username'], _id=session['user_id'])
    return render_template('forms/EditForm/edit_page.html', form=user.get_job_by_row_id(str(value)))

@app.route('/delete/<row>')
@login_required
def delete(row):
    """deletes data from the a specific row"""
    user = User(session['username'], _id=session['user_id'])
    user.delete_job(row)
    return redirect(request.referrer)

@app.route('/admin')
@login_required
def admin_login():
    """Changes the user from normal user to admin"""
    session['username'] = 'admin'
    return redirect(url_for('history'))

@app.route('/user')
@login_required
def user_login():
    """Logs the user into the user home page"""
    session['username'] = session['session_name']
    return redirect(url_for('history'))


@app.route('/search', methods=('GET', 'POST'))
@login_required
def search():
    """Search form that allows the user to search the form based on the job attributes"""

    # FIX THE CODE REQUIRING THE RADIO BUTTONS
    #title  = request.form.get('jobInfo')
    form = SearchForm()
    error = ''
    if request.method == 'POST':
        if form.validate_on_submit:
            search_form = ValidateSearchForm(form)
            jobs = search_form.get_data()
            if jobs:
                global SEARCH_FORM_JOBS
                SEARCH_FORM_JOBS = jobs
                return redirect(url_for('perma_link'))
        error = 'No records find by that entry'
        return render_template('forms/SearchPageForm/search_page.html', form=form, error=error)
    return render_template('forms/SearchPageForm/search_page.html', form=form)

@app.route('/.json')
@app.route('/home.json')
@app.route('/history/jobs.json')
@app.route('/active/jobs.json')
@app.route('/job/entry.json')
@app.route('/search.json')
@login_required
def get_json():
    """gets the json representation of the data"""
    user = User(session['username'], _id=session['user_id'])
    return render_template('json/json.html', records=user.to_json(), json=json.dumps)

@app.route('/home')
@login_required
def home():
    """returns the user to home screen"""
    return render_template('home_page/home_page.html')

@app.route('/faq')
@login_required
def faq():
    """renders the FAQ to the user"""
    return render_template('faq/faq.html')

@app.route('/secret/questions', methods=('GET', 'POST'))
def register_secret_questions_answers():

    form = ForgottenPasswordForm()
    if form.validate_on_submit():
        user = User(session['username'], _id=session['user_id'])
        user.save_secret_answers(form, session['username'])
        return redirect('login')
    return render_template('forms/SecretQuestions/secret_questions_registration.html',
                           form=form,
                           username=session['username'])

@app.route('/secret/questions/answers', methods=('GET', 'POST'))
def forgotten_password():
    """
    """
    form  = ForgottenPasswordForm()
    error = ''
    if form.validate_on_submit():
        user_answers = ValidiateSecretQuestions(form)
        if user_answers.validate_answers():
            session['username'] = form.username.data.lower()
            return redirect(url_for('new_password'))
        error = 'The user was not found'
    return render_template('forms/SecretQuestions/secret_questions_answers.html', form=form, error=error)

@app.route('/newpassword', methods=('GET', 'POST'))
def new_password():
    """
    """
    form = NewPasswordForm()
    if form.validate_on_submit():
        user = User(session['username'])
        hash_password = create_passwd_hash(str(form.password.data))
        user.update_password(session['username'], hash_password)
        user_id = user.get_user_id(session['username'])
        session['user_id'] = user_id
        session['session_name'] = session['username']
        return redirect('login')
    return render_template('forms/NewPasswordsForm/new_password_form.html', form=form)
