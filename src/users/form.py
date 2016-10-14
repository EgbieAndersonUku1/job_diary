##################################################################
# Author : Egbie Uku
# Creates the tables or rows necessary for the Web interface
##################################################################

from flask_wtf import Form
from wtforms import validators, StringField, PasswordField
from wtforms.fields.html5 import EmailField

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
