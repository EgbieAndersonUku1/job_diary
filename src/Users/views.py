#-*- coding: utf-8 -*-
#####################################################################
# Author = Egbie Uku
#####################################################################

# ADD BLUEPRINTS HERE MOVE SOME OF THESE IMPORTED MODULES TO THEIR APPROPRIATE
# VIEW FILES
import json
import datetime
import uuid
from src.Users.Models.Caches.cache import Cache
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
from src.Users.registration_and_login_helper import login_user, register_user
from src.utilities.password_hasher import create_passwd_hash
from src.Users.user import User
from src.Users.Jobs.job_evaluator import Evaluator
from src.Users.Models.TotalUserMoneys.total_amount import TotalAmount
from src.Users.Jobs.job_helper import ( get_jobs,
                                        is_shift_now,
                                        is_shift_over,
                                        is_shift_confirmed,
                                        when_is_shift_starting)


@app.before_first_request
def initialize():
    """initialize the database"""
    DataBase.initialize()


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
