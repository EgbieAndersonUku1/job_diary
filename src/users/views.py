from src.users.form import RegisterForm, LoginForm, AdminRegisterForm, AdminLoginForm
from job_diary import app
from flask import render_template, session, redirect, url_for, flash, request
from user_form_helpers import login_helper, register_helper
import datetime
from src.users.models import ProcessForm
from src.models.users import User, Records
import uuid
from src.users.decorators import login_required, admin_required
from time import sleep

date = datetime.datetime.now()
curr_day = datetime.date.today().strftime("%A")
curr_date = "{}/{}/{}".format(date.day, date.month, date.year)

# use the _login_helper to log the user in
@app.route('/', methods=('GET', 'POST'))
@app.route('/login', methods=('GET', 'POST'))
def login():
    """Allows the user entry to the login applicaton"""
    return login_helper(LoginForm, 'username', 'entry_page', 'user/login.html', 'index', False)

# use the login helper to help assist the user in logging into admin console
@app.route('/admin/', methods=('GET', 'POST'))
@app.route('/admin/login', methods=('GET', 'POST'))
def admin():
    """Allows the user entry as admin"""
    return login_helper(AdminLoginForm, 'admin', 'success', 'admin/admin_login.html', 'index', True)

# admin registration
@app.route('/admin/register', methods=('GET', 'POST'))
def admin_register():
    return register_helper(AdminRegisterForm, 'Incorrect admin name', 'admin/admin.html', 'success')

# user registration
@app.route('/register', methods=('GET', 'POST'))
def user_register():
    return register_helper(RegisterForm, 'username must be unique', 'user/registration.html', 'entry_page')

@app.route('/success')
@login_required
def success():
    return 'some text will be here'

@app.route('/job/entry', methods=('GET', 'POST'))
@login_required
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
        # process the user information
        user_form = ProcessForm(title, descr, loc, hourly_rate,start_date, end_date,
                                start_hours, start_mins, end_hours, end_mins, day)
        # if the user details are sucessful add the details for the job to the database
        success, errors, form = user_form.verify_form()
        if success:
            row = user_form.process_form(start_date, end_date, day)
            return redirect(url_for('success_page', row=row))

        return render_template('user/entry_page.html',start_date=form.start_date, end_date=form.end_date,
                               job_title=form.job_title, description=form.description, location=form.location,
                               start_hours=form.start_hours, day=day,
                               start_mins=form.start_mins, rate=form.rate,end_hours=form.end_hours,
                               end_mins=form.end_mins, errors=errors)

@app.route('/index', methods=('GET', 'POST'))
def index():
    if session.get('username', None):
        return 'hello'
    elif session.get('admin', None):
        return 'hello, admin'
    else:
        return (redirect(url_for('login')))

@app.route('/logout')
@login_required
def logout():
    if session.get('admin'):
        session['admin'] = None
    else:
        session['username'] = None
    session['user_id'] = None
    return (redirect(url_for('login')))

@app.route('/reset')
def reset():
    return render_template('user/entry_page.html', start_date=curr_date, end_date=curr_date, day=curr_day)

@app.route('/successful/<row>')
@login_required
def success_page(row):

   user = User('',_id=session['user_id'])
   rows = user.get_by_row_id(row)
   flash('The following data has been successful added to the database.')
   return render_template('user/table.html', rows=rows)

@app.route('/history')
@login_required
def get_dates():
    user = User(session['username'], _id=session['user_id'])
    # some varialbe to contr
    jobs = user.get_by_user_id(100) # some code here to limit how much is display in history
    return render_template('user/history.html', jobs=jobs, date=curr_date, dt=datetime.datetime.strptime)

@app.route('/job/edit/<value>')
def edit(value):
    user = User(session['username'], _id=session['user_id'])
    form = user.get_by_row_id(str(value))
    return render_template('user/edit.html', form=form)

@app.route('/delete/<row>')
@login_required
def delete(row):
    user = User(session['username'], _id=session['user_id'])
    print user.delete_row(row)
    return redirect(url_for('get_dates'))
