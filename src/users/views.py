from src.users.form import RegisterForm, LoginForm, AdminRegisterForm, AdminLoginForm
from job_diary import app
from flask import render_template, session, redirect, url_for, flash, request
from user_form_helpers import login_helper, register_helper
import datetime

date = datetime.datetime.now()
curr_date = "{}/{}/{}".format(date.day, date.month, date.year)

# use the _login_helper to log the user in
@app.route('/', methods=('GET', 'POST'))
@app.route('/login', methods=('GET', 'POST'))
def login():
    """Allows the user entry to the login applicaton"""
    error = 'Incorrect username and password'
    return login_helper(LoginForm, error, 'username', 'success', 'user/login.html', 'index', False)

# use the login helper to help assist the user in logging into admin console
@app.route('/admin/', methods=('GET', 'POST'))
@app.route('/admin/login', methods=('GET', 'POST'))
def admin():
    """Allows the user entry as admin"""

    error = 'Incorrect username your IP will be logged'
    return login_helper(AdminLoginForm, error, 'admin', 'success', 'admin/admin_login.html', 'index', True)

# admin registration
@app.route('/admin/register', methods=('GET', 'POST'))
def admin_register():
    return register_helper(AdminRegisterForm, 'Incorrect admin name', 'admin/admin.html', 'success')

# user registration
@app.route('/register', methods=('GET', 'POST'))
def user_register():
    return register_helper(RegisterForm, 'username must be unique', 'user/registration.html', 'success')


@app.route('/success')
def success():
    return 'hello'

@app.route('/job/entry', methods=('GET', 'POST'))
def entry_page():

    start_date, end_date = curr_date, curr_date

    if request.method == 'GET':
        return render_template('user/entry_page.html', start_date=start_date, end_date=end_date)
    else:
        job_title   = request.form.get('job_title')
        job_descr   = request.form.get('description')
        job_loc     = request.form.get('location')
        hourly_rate = request.form.get('hourly_rate')
        start_date  = request.form.get('start_date')
        end_date    = request.form.get('end_date')
        start_hours = request.form.get('start_hours')
        start_mins  = request.form.get('start_mins')
        end_hours   = request.form.get('end_hours')
        end_mins    = request.form.get('end_mins')


    return render_template('user/entry_page.html', start_date=start_date, end_date=end_date)



@app.route('/index', methods=('GET', 'POST'))
def index():
    if session.get('username', None):
        return 'hello'
    elif session.get('admin', None):
        return 'hello, admin'
    else:
        return (redirect(url_for('login')))

@app.route('/logout')
def logout():
    if session.get('admin'):
        session['admin'] = None
    else:
        session['username'] = None
    return (redirect(url_for('login')))

@app.route('/reset')
def reset():
    return render_template('user/entry_page.html', start_date=curr_date, end_date=curr_date)
