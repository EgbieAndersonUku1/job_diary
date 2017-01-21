###############################################################################
# Author; Egbie
###############################################################################

from flask import Blueprint
from src.Users.registration_and_login_helper import register_user
from src.Users.Forms.login_form import RegisterForm

user_registration = Blueprint('user_registration', __name__)

@user_registration.route('/register', methods=('GET', 'POST'))
def user_register():
    """Register the user to the application"""
    form = RegisterForm()
    return register_user(form=form,
                         error='username must be unique',
                         template='forms/LoginRegistrationForm/registration.html',
                         redirect_link='home')
