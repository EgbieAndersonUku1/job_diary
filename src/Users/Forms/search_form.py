#################################################################
# Author : Egbie Uku
# Creates the tables or rows necessary for the Web interface
##################################################################

from flask_wtf import Form
from wtforms import validators, StringField, DecimalField

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
    
