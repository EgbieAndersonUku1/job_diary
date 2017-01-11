##############################################################################
# Author: Egbie
##############################################################################

from flask import session, redirect, url_for, Blueprint
from src.Users.registration_and_login_helper import login_user
from src.Users.Forms.login_form import LoginForm

url_admin_redirect = Blueprint('login_admin_redirect', __name__)
url_login_redirect  = Blueprint('login_user_redirect', __name__)
login_user = Blueprint('login_user', __name__)
logout_user = Blueprint('logout_user', __name__)

@url_admin_redirect.route('/admin')
@login_required
def admin_login_redirect():
    """Allows the user to redirect to history page whenever the user
       clicks their admin link.
    """
    session['username'] = 'admin'
    return redirect(url_for('history.job_histories'))

@url_login_redirect.route('/user')
@login_required
def user_login_redirect():
    """Allows the user to redirect to history page whenever the user
       clicks their user link name.
    """
    session['username'] = session['session_name']
    return redirect(url_for('history.job_histories'))

@login_user.route('/', methods=('GET', 'POST'))
@login_user.route('/login', methods=('GET', 'POST'))
def login():
    """Allows the user entry into the login applicaton"""
    form = LoginForm()
    return login_user(form=form,
                      session_name='username',
                      redirect_link='home',
                      template='forms/LoginRegistrationForm/login.html',
                      index='home')

@logout_user.route('/logout')
@login_required
def logout():
    """log the user out of the application"""
    if session.get('admin', None):
        session.pop('admin')
    session.pop('username')
    session.pop('user_id')
    session.pop('session_name')
    return redirect(url_for('login_user.login'))
