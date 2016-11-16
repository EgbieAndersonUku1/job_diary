#-*- coding: utf-8 -*-
from src.users.form import RegisterForm, LoginForm, SearchForm
from job_diary import app
from flask import render_template, session, redirect, url_for, flash, request
from user_form_helpers import login_helper, register_helper
import datetime
from src.users.models import ProcessForm, ProcessSearchForm
from src.models.users import User, Records
from src.models.utils import get_daily_rate, time_to_str, get_hours_worked, time_to_float, month_to_str
import uuid
from src.users.decorators import login_required, admin_required
from flask_paginate import Pagination
from src.models.database import DataBase
import json

@app.before_first_request
def initialize():
    DataBase.initialize()

date = datetime.datetime.now()
curr_day = datetime.date.today().strftime("%A")
curr_date = "{}-{}-{}".format(date.year, date.month, date.day)


# use the _login_helper to log the user in
@app.route('/', methods=('GET', 'POST'))
@app.route('/login', methods=('GET', 'POST'))
def login():
    """Allows the user entry to the login applicaton"""
    return login_helper(LoginForm, 'username', 'home', 'user/login.html', 'home')

# user registration
@app.route('/register', methods=('GET', 'POST'))
def user_register():
    return register_helper(RegisterForm, 'username must be unique', 'user/registration.html', 'home')


@app.route('/job/entry', methods=('GET', 'POST'))
@login_required
def entry_page():
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

    if request.method == 'GET':
        return render_template('user/entry_page.html',start_date=start_date, end_date=end_date, day=day,
                               job_title=title, description=descr, location=loc, start_hours=start_hours,
                               start_mins=start_mins, rate=hourly_rate,end_hours=end_hours,end_mins=end_mins, errors='',
                               success='')
    else:
        # process the user information
        user_form = ProcessForm(title, descr, loc, hourly_rate,start_date, end_date, start_hours, start_mins, end_hours, end_mins, day)
        success, errors, form = user_form.verify_form() # if job details are sucessful add to the database
        if success:
            return redirect(url_for('success_page', row=user_form.process_form(start_date, end_date, day)))
        return render_template('user/entry_page.html',start_date=form.start_date, end_date=form.end_date,
                               job_title=form.job_title, description=form.description, location=form.location,
                               start_hours=form.start_hours, day=day,
                               start_mins=form.start_mins, rate=form.rate,end_hours=form.end_hours,
                               end_mins=form.end_mins, errors=errors)

@app.route('/logout')
@login_required
def logout():
    if session.get('admin', None):
        session.pop('admin')
    session.pop('username')
    session.pop('user_id')
    session.pop('session_name')
    return (redirect(url_for('login')))

@app.route('/reset')
@login_required
def reset():
    return render_template('user/entry_page.html', start_date=curr_date, end_date=curr_date, day=curr_day)

@app.route('/successful/<row>')
@login_required
def success_page(row):

   user = User('',_id=session['user_id'])
   flash('The following data has been successful added to the database.')
   return render_template('user/table.html', rows=user.get_by_row_id(row))

def _get_jobs(active_jobs):
    user = User(session['username'], _id=session['user_id'])
    jobs, total_pay, total_hrs, worked_jobs =  user.get_by_user_id(), [], [], []

    def get_jobs_helper(daily_rate, hrs, job):
        total_pay.append(float(job.daily_rate))
        total_hrs.append(float(job._hours))
        worked_jobs.append(job)

    # get the jobs that we have already worked
    for job in jobs:
        if not active_jobs:
            if datetime.datetime.strptime(job.date, "%Y-%m-%d") < datetime.datetime.strptime(curr_date, "%Y-%m-%d"):
                get_jobs_helper(job.daily_rate, job._hours, job)
        elif active_jobs and datetime.datetime.strptime(job.date, "%Y-%m-%d") >= datetime.datetime.strptime(curr_date, "%Y-%m-%d"):
                get_jobs_helper(job.daily_rate, job._hours, job)
    return jobs, total_pay, total_hrs, worked_jobs

def _display(html_link, active=False):
    """_display(str, str) -> return(value)

    @params:
    html_link: The link of the page to render
    active   : Whether the jobs are active e.g not worked yet.
    returns  : Render object.

    Renders the jobs worked or not worked along with the hours and total pay.
    """
    jobs, total_pay, total_hrs, worked_jobs = _get_jobs(active_jobs=active)
    return render_template(html_link, jobs=worked_jobs, date=curr_date,
                            translate=month_to_str,
                            dt=datetime.datetime.strptime,
                            total_pay=sum(total_pay),
                            total_hrs=int(round(sum(total_hrs))), active=active)


@app.route('/history/jobs',  methods=('GET', 'POST'))
@login_required
def history():
    return _display('user/history.html')

@app.route('/active/jobs', methods=('GET', 'POST'))
@login_required
def active_jobs():
    return _display('user/active_jobs.html', True)

@app.route('/job/edit/<value>')
@login_required
def edit(value):
    user = User(session['username'], _id=session['user_id'])
    return render_template('user/edit.html', form=user.get_by_row_id(str(value)))

@app.route('/delete/<row>')
@login_required
def delete(row):
    user = User(session['username'], _id=session['user_id'])
    user.delete_row(row)
    return redirect(request.referrer)

@app.route('/admin')
@login_required
def admin_login():
    session['username'] = 'admin'
    return redirect(url_for('history'))

@app.route('/user')
@login_required
def user_login():
    session['username'] = session['session_name']
    return redirect(url_for('history'))

@app.route('/index', methods=('GET', 'POST'))
@app.route('/search', methods=('GET', 'POST'))
@login_required
def search():

    # FIX THE CODE SO THAT IT USES VALUES FROM THE RADIO BUTTONS
    #title  = request.form.get('jobInfo')
    form = SearchForm()
    error = ''
    if request.method == 'POST':
        if form.validate_on_submit:
            search_form = ProcessSearchForm(form)
            jobs = search_form.get_data()
            if jobs:
                total_hrs, total_pay = [], []
                for job in jobs:
                    total_pay.append(float(job.daily_rate))
                    total_hrs.append(float(job._hours))
                return render_template("user/permalink_jobs_history.html", jobs=jobs,
                                        translate=month_to_str, total_pay=sum(total_pay),
                                        total_hrs=sum(total_hrs), curr_date=curr_date,
                                        dt=datetime.datetime.strptime)
            else:
                error = 'No records find by that entry'
                return render_template('user/search.html', form=form, error=error)
    else:
        return render_template('user/search.html', form=form)


@app.route('/.json')
@app.route('/home.json')
@app.route('/history/jobs.json')
@app.route('/active/jobs.json')
@app.route('/job/entry.json')
@app.route('/search.json')
@login_required
def get_json():
    user = User(session['username'], _id=session['user_id'])
    return render_template('user/json.html', records=user.get_records(), json=json.dumps)

@app.route('/update/<row>')
@login_required
def update(row):
    # FIX THE UPDATE METHOD
    pass

@app.route('/home')
@login_required
def home():
    return render_template('user/home_page.html')
