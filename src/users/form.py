#################################################################
# Author : Egbie Uku
# Creates the tables or rows necessary for the Web interface
##################################################################

from flask_wtf import Form
from wtforms import validators, StringField, PasswordField, DecimalField, RadioField
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileField, FileAllowed

class RegisterForm(Form):
    """RegisterForm(class)
    Allows the user of the application to register their
    details to the database.
    """
    email     = EmailField('Email', [validators.Required()])
    password  = PasswordField('New Password', [validators.Required(),
                                               validators.Length(min=4,max=80),
                                               validators.EqualTo('confirm',
                                               message='password does not match')])
    confirm   = PasswordField('Repeat Password')

class LoginForm(Form):
    """LoginForm(class)
    Allows the user to gain access to the program via the login inteface.
    """
    username = EmailField('Username', [validators.Required()])
    password = PasswordField('Password',[validators.Required(), 
                                        validators.Length(min=4, max=80)])
class SearchForm(Form):
    """SearchForm(class)
    Allows the user to search the database based on the job attributes e.g. title,
    location, month, etc via a form interface.
    """

    year = StringField('Year', [validators.Length(max=4)])
    job_title = StringField('Job title',[validators.Length(max=255)])
    location  = StringField('Location ', [validators.Length(max=255)])
    hrs_worked = StringField('Hours worked', [validators.Length(max=4)])
    month  = StringField('Month ', [validators.Length(max=16)])
    date      = StringField('Date')
    day       = StringField('Weekday', [validators.Length(max=9)])
    start_time = StringField('Start time')
    finish_time = StringField('Finish time')
    daily_rate  = DecimalField('Daily rate', rounding=2)
    month_one = StringField('From', [validators.Length(max=17)])
    month_two = StringField('To', [validators.Length(max=17)])
    job_confirmation = StringField('Shift/Job Confirmation (yes/no)', [validators.Length(max=3)])
    
class ForgottenPasswordForm(Form):
    """ForgottenForm(class)
    Allows the user to retreive their forgotten password.
    """
    username = StringField('Enter your login username.', 
                          [validators.Length(max=80)])
    maiden_name = StringField('What is your mother maiden name ?', 
                               [validators.Required(), 
                               validators.Length(max=80)])
    leisure = StringField('What is your favourite activity ?', [validators.Required(), 
                                                                validators.Length(max=80)])
class NewPasswordForm(Form):
    """NewPasswordForm(class)
    """
    password = PasswordField('New password', 
                           [validators.Required(),
                           validators.Length(min=4, max=80),
                           validators.EqualTo('confirm', message='password does not match')])
    confirm = PasswordField('Repeat password')