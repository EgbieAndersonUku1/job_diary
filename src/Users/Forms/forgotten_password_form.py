#################################################################
# Author : Egbie Uku
# Creates the tables or rows necessary for the Web interface
##################################################################

from flask_wtf import Form
from wtforms import validators, StringField

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
