##################################################################
# Author : Egbie Uku
# Creates the tables or rows necessary for the Web interface
##################################################################

from flask_wtf import Form
from wtforms import validators, StringField, PasswordField, DecimalField
from wtforms.fields.html5 import EmailField
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_wtf.file import FileField, FileAllowed

class RegisterForm(Form):
    """RegisterForm(class)
    Allows the user of the application to register their
    details to the database.
    """
    email     = EmailField('Email', [validators.Required()])
    password  = PasswordField('New Password', [validators.Required(),
                                               validators.Length(min=4,max=80),
                                               validators.EqualTo('confirm', message='password does not match')])
    confirm   = PasswordField('Repeat Password')

class LoginForm(Form):
    """LoginForm(class)
    Allows the user to gain access to the program via the login inteface.
    """
    username = EmailField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required(), validators.Length(min=4, max=80)])

class SearchForm(Form):
    """SearchForm(class)
    Allows the user to search for jobs based on their, location, date, hourly
    rate, etc
    """

    job_title = StringField('Job title (Optional)',[validators.Length(max=255)])
    location  = StringField('Location (Optional)', [validators.Length(max=255)])
    hrs_worked = StringField('Hours worked (Optional : Enter as decimal. e.g 3 hrs and 15 mins enter as 3.15, 4 hrs as 4.0)', [validators.Length(max=4)])
    month  = StringField('Month (Optional)', [validators.Length(max=16)])
    date      = StringField('Date (Optional)')
    day       = StringField('Weekday (Optional)', [validators.Length(max=9)])
    start_time = StringField('Start time (Optional)')
    finish_time = StringField('Finish time (Optional)')
    daily_rate  = DecimalField('Daily rate (Optional)', rounding=2)
