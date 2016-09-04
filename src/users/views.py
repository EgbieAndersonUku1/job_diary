from src.users.form import RegisterForm, LoginForm, AdminRegisterForm, AdminLoginForm
from job_diary import app
from flask import render_template, session, redirect, url_for, flash, request
from user_form_helpers import login_helper, register_helper
import datetime
from src.users.models import ProcessForm
from src.models.users import User

date = datetime.datetime.now()
curr_day = datetime.date.today().strftime("%A")
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

    if request.method == 'GET':
        return render_template('user/entry_page.html',start_date=start_date, end_date=end_date, day=day,
                               job_title=title, description=descr, location=loc, start_hours=start_hours,
                               start_mins=start_mins, rate=hourly_rate,end_hours=end_hours,end_mins=end_mins, errors='',
                               success='')
    else:
        # ADD A FUNCTION HERE TO PROCESS THE FORM BEFPRE STORING IN THE database
        user_form = ProcessForm(title, descr, loc, hourly_rate, start_date, end_date, start_hours, start_mins, end_hours, end_mins)
        success, errors, form = user_form.verify_form()
        if success:
            start_time = form.start_hours + ':' + form.start_mins
            finish_time   = form.end_hours +   ":" + form.end_mins
            user = User('', start_date, end_date, day)
            user.add_job_details(form.job_title, form.description,
                                 form.location, start_time,
                                 finish_time, form.rate)
            success = 'Your data has been added to the database.'
            #user_records = Records(form.job_title, form.description, form.location, start_time, finish_time, form.rate)

        # ADD A FLASHING MESSAGE TO TELL THE USERS THAT THEIR DATA HAS SUCCESS BEEN ADDED TO DATABASE
        # return render_template('user/entry_page.html', user_form=form)
        return render_template('user/entry_page.html',start_date=form.start_date, end_date=form.end_date,
                               job_title=form.job_title, description=form.description, location=form.location,
                               start_hours=form.start_hours, day=day,
                               start_mins=form.start_mins, rate=form.rate,end_hours=form.end_hours,
                               end_mins=form.end_mins, errors=errors, success=success)

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
    return render_template('user/entry_page.html', start_date=curr_date, end_date=curr_date, day=curr_day)
