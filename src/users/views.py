#-*- coding: utf-8 -*-
from src.users.form import RegisterForm, LoginForm, SearchForm
from job_diary import app
from flask import render_template, session, redirect, url_for, flash, request
from _user_form_helper import login_user, register_user
from src.users.process_forms import ProcessForm, ProcessSearchForm
from src.models.users import User
from src.utilities.job_processor import (get_daily_rate, 
                                         get_hours_worked, get_jobs, 
                                         is_shift_now, 
                                         is_shift_over,
                                         is_shift_confirmed,
                                         when_is_shift_starting)

from src.utilities.time_processor import time_to_str, convert_mins_to_hour
from src.utilities.date_month_day_processor import month_to_str
from src.users.decorators import login_required, admin_required
from src.models.database import DataBase
from flask_paginate import Pagination
import json
import datetime
import uuid

date = datetime.datetime.now()
curr_day = datetime.date.today().strftime("%A")
curr_date = "{}-{}-{}".format(date.year, date.month, date.day)

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
                      template='login_and_registration/login.html',
                      index='home')

@app.route('/register', methods=('GET', 'POST'))
def user_register():
    """Register the user to the application"""
    form = RegisterForm()
    return register_user(form=form,
                         error='username must be unique', 
                         template='login_and_registration/registration.html', 
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
        return render_template('forms/job_entry_page.html',
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

    user_form = ProcessForm(title, descr, loc, 
                            hourly_rate, start_date, 
                            end_date, start_hours, 
                            start_mins, end_hours, 
                            end_mins, day, is_shift_confirmed)
    success, errors, form = user_form.verify_form() 
    if success:
        # row_ID comes from the form so False is expressed as unicode
        # instead of a boolean. This make the if-condition 
        # if row_ID == False always True instead of False.
        # By expressing it as str(row_ID) != 'False' it makes the if-statement
        # False when the string returned is not equal to the string False.
        if str(row_ID) != 'False': # means the row should be updated.
            row_id = user_form.process_form(start_date, end_date, day, row_ID, update=True)
        else:
            row_id = user_form.process_form(start_date, end_date, day)
        return redirect(url_for('success_page', row_id=row_id)) 
    return render_template('forms/job_entry_page.html',
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

@app.route('/reset')
@login_required
def reset():
    """reset the value in the form for the application"""
    return render_template('forms/job_entry_page.html', 
                            start_date=curr_date, 
                            end_date=curr_date, 
                            day=curr_day)

@app.route('/successful/<row_id>')
@login_required
def success_page(row_id):
   """redirects the user to successful page entry after successful input"""
   user = User('',_id=session['user_id'])
   flash('The data below has been added to the database.')
   return render_template('render_to_user/table.html', rows=user.get_by_row_id(row_id))

def _display(html_link, active=False):
    """_display(str, str) -> return(value)

    @params:
    html_link: The link of the page to render
    active   : Whether the jobs are active e.g not worked yet.
    returns  : Render object.

    Renders the jobs worked or not worked along with the hours and total pay.
    """
    jobs, total_pay, total_hrs, worked_jobs = get_jobs(active, User, session, curr_date)
    user = User(session['username'], _id=session['user_id'])
    page = request.args.get('page', type=int, default=1)
    pagination = Pagination(page=page, total=len(worked_jobs), 
                            record_name='history', 
                            per_page=10, 
                            format_total=True, 
                            link_size='lg')
    
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
                           delete=user.delete_row,
                           len=len,
                           pagination=pagination)

@app.route('/history/jobs', methods=('GET', 'POST'))
@login_required
def history():
    """renders the entire job history active and none active"""
    return _display('worked_jobs/jobs_history.html')
    
@app.route('/active/jobs', methods=('GET', 'POST'))
@login_required
def active_jobs():
    """renders the all jobs that are active (not worked)"""
    return _display('current_jobs/current_jobs.html', True)

@app.route('/job/edit/<value>')
@login_required
def edit(value):
    """Allows the jobs to be edited"""
    user = User(session['username'], _id=session['user_id'])
    return render_template('forms/edit_page.html', form=user.get_by_row_id(str(value)))

@app.route('/delete/<row>')
@login_required
def delete(row):
    """deletes data from the a specific row"""
    user = User(session['username'], _id=session['user_id'])
    user.delete_row(row)
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

@app.route('/index', methods=('GET', 'POST'))
@app.route('/search', methods=('GET', 'POST'))
@login_required
def search():
    """Search form that allows the user to search the form based on the job attributes"""
    
    # FIX THE CODE SO THAT IT USES VALUES FROM THE RADIO BUTTONS AND NOT ALL VALUES
    #title  = request.form.get('jobInfo')
    user = User(session['username'], _id=session['user_id'])
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
                return render_template("render_to_user/perma_link.html", 
                                        jobs=jobs,
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
                                        delete=user.delete_row,
                                        len=len)
            error = 'No records find by that entry'
            return render_template('forms/search_page.html', form=form, error=error)
    return render_template('forms/search_page.html', form=form)

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