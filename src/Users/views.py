#-*- coding: utf-8 -*-
import json
import datetime
import uuid
from src.utilities.time_processor import time_to_str, convert_mins_to_hour
from src.utilities.date_month_day_processor import month_to_str
from src.models.Registrations.registration import Registration
from src.models.Databases.database import DataBase
from src.Users.decorators import login_required, admin_required
from flask_paginate import Pagination
from src.Users.Validator.validate_secret_questions import ValidiateSecretQuestions
from src.Users.Validator.validate_search_form import ValidateSearchForm
from src.Users.Forms.register_form import RegisterForm
from src.Users.Forms.login_form import LoginForm
from src.Users.Forms.search_form import SearchForm
from src.Users.Forms.forgotten_password_form import ForgottenPasswordForm
from src.Users.Forms.new_password_form import NewPasswordForm
from job_diary import app
from flask import render_template, session, redirect, url_for, flash, request
from _form_helper import login_user, register_user
from src.Users.Validator.validate_job_details_form import ValidateJobDetailsForm
from src.utilities.common import create_passwd_hash
from src.Users.user import User
from src.utilities.job_processor import (get_daily_rate,
                                         get_hours_worked, get_jobs,
                                         is_shift_now,
                                         is_shift_over,
                                         is_shift_confirmed,
                                         when_is_shift_starting)
date = datetime.datetime.now()
curr_day = datetime.date.today().strftime("%A")
curr_date = "{}-{}-{}".format(date.year, date.month, date.day)
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
                      template='forms/loginRegistrationForm/login.html',
                      index='home')

@app.route('/register', methods=('GET', 'POST'))
def user_register():
    """Register the user to the application"""
    form = RegisterForm()
    return register_user(form=form,
                         error='username must be unique',
                         template='forms/loginRegistrationForm/registration.html',
                         redirect_link='home')

@app.route('/job/entry/<row_ID>', methods=('GET', 'POST'))
@login_required
def entry_page(row_ID):
    """entry_page(func)
    Retreives and process the users data. Also renders the user data
    from the entry job page.
    """
    start_date, end_date = curr_date, curr_date
    title   = request.form.get('job_title', '')
    descr   = request.form.get('description', '')
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
                                      end_date, start_hours,
                                      start_mins, end_hours,
                                      end_mins, day, is_shift_confirmed)
    success, errors, form = job_form.verify_form()
    if success:
        # row_ID comes from the form so False is expressed as unicode
        # instead of a boolean. This make the if-condition
        # if row_ID == False always True instead of False.
        # By expressing it as str(row_ID) != 'False' it makes the if-statement
        # False when the string returned is not equal to the string False.
        if str(row_ID) != 'False': # means the row should be updated.
            row_id = job_form.process_form(start_date, end_date, day, row_ID, update=True)
        else:
            row_id = job_form.process_form(start_date, end_date, day)
        return redirect(url_for('success_page', row_id=row_id))
    return render_template('forms/JobEntryForm/job_entry_page.html',
                           start_date=form.start_date,
                           end_date=form.end_date,
                           job_title=form.job_title,
                           description=form.description,
                           location=form.location,
                           start_hours=form.start_hours,
                           day=day,
                           start_mins=form.start_mins,
                           rate=form.rate,
                           end_hours=form.end_hours,
                           end_mins=form.end_mins,
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

@app.route('/successful/<row_id>')
@login_required
def success_page(row_id):
   """redirects the user to successful page entry after successful input"""
   user = User(session['username'],_id=session['user_id'])
   flash('The data below has been added to the database.')
   return render_template('forms/permalinks/perma_table.html', rows=user.get_job_by_row_id(row_id))

def _display(html_link, active=False):
    """_display(str, str) -> return(value)

    :parameters
        - html_link: The link of the page to render
        - active   : Whether the jobs are active e.g not worked yet.
        - returns  : Render object.

    Renders the jobs worked or not worked along with the hours and total pay.
    """
    jobs, total_pay, total_hrs, worked_jobs = get_jobs(active, User, session, curr_date)
    user = User(session['username'], _id=session['user_id'])
    page = request.args.get('page', type=int, default=1)
    return render_template(html_link,
                           jobs=worked_jobs,
                           date=curr_date,
                           translate=month_to_str,
                           dt=datetime.datetime.strptime,
                           total_pay=round(sum(total_pay),2),
                           total_hrs=round(sum(total_hrs), 2),
                           active=active,
                           is_shift_over=is_shift_over,
                           converter=convert_mins_to_hour,
                           when_is_shift_starting=when_is_shift_starting,
                           is_shift_now=is_shift_now,
                           is_shift_confirmed=is_shift_confirmed,
                           delete=user.delete_job,
                           len=len)

@app.route('/history/jobs', methods=('GET', 'POST'))
@login_required
def history():
    """renders the entire job history active and none active"""
    return _display('forms/worked_jobs/jobs_history.html')

@app.route('/active/jobs', methods=('GET', 'POST'))
@login_required
def active_jobs():
    """renders the all jobs that are active (not worked)"""
    return _display('forms/current_jobs/current_jobs.html', True)

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

@app.route('/search/permalinks/jobs')
def perma_link():
    """Displays the jobs retreived from the search function"""

    user = User(session['username'], _id=session['user_id'])
    total_hrs, total_pay = [], []

    for job in SEARCH_FORM_JOBS: # calculate the hours and wages from the jobs retreived.
        total_pay.append(float(job.daily_rate))
        total_hrs.append(float(job._hours))
    return render_template("forms/permalinks/perma_link.html",
                            jobs=SEARCH_FORM_JOBS,
                            translate=month_to_str,
                            total_pay=sum(total_pay),
                            total_hrs=sum(total_hrs),
                            curr_date=curr_date,
                            dt=datetime.datetime.strptime,
                            is_shift_now=is_shift_now,
                            is_shift_over=is_shift_over,
                            converter=convert_mins_to_hour,
                            when_is_shift_starting=when_is_shift_starting,
                            is_shift_confirmed=is_shift_confirmed,
                            delete=user.delete_job,
                            len=len)

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
