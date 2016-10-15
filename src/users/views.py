from src.users.form import RegisterForm, LoginForm
from job_diary import app
from flask import render_template, session, redirect, url_for, flash, request
from user_form_helpers import login_helper, register_helper
import datetime
from src.users.models import ProcessForm
from src.models.users import User, Records
import uuid
from src.users.decorators import login_required, admin_required
from src.models.utils import translate_month

date = datetime.datetime.now()
curr_day = datetime.date.today().strftime("%A")
curr_date = "{}/{}/{}".format(date.day, date.month, date.year)

# use the _login_helper to log the user in
@app.route('/', methods=('GET', 'POST'))
@app.route('/login', methods=('GET', 'POST'))
def login():
    """Allows the user entry to the login applicaton"""
    return login_helper(LoginForm, 'username', 'entry_page', 'user/login.html', 'index')

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
        user_form = ProcessForm(title, descr, loc, hourly_rate,start_date, end_date, start_hours, start_mins, end_hours, end_mins, day)
        success, errors, form = user_form.verify_form() # if job details are sucessful add to the database
        if success:
            return redirect(url_for('success_page', row=user_form.process_form(start_date, end_date, day)))
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
    return (redirect(url_for('login')))

@app.route('/logout')
@login_required
def logout():
    if session.get('admin', None):
        session.pop('admin')
    session.pop('username')
    session.pop('user_id')
    session.pop('session_name')
    return (redirect(url_for('login')))

@app.route('/reset')
def reset():
    return render_template('user/entry_page.html', start_date=curr_date, end_date=curr_date, day=curr_day)

@app.route('/successful/<row>')
@login_required
def success_page(row):

   user = User('',_id=session['user_id'])
   flash('The following data has been successful added to the database.')
   return render_template('user/table.html', rows=user.get_by_row_id(row))

@app.route('/history')
@login_required
def history():
    user = User(session['username'], _id=session['user_id'])
    # some code here to limit how much is display in history
    jobs, total_pay, total_hrs =  user.get_by_user_id(100), [], []

    for job in jobs:
        total_pay.append(float(job.daily_rate))
        total_hrs.append(float(job._hours))

    return render_template('user/history.html', jobs=jobs, date=curr_date, translate=translate_month,
                            dt=datetime.datetime.strptime, total_pay=sum(total_pay),
                            total_hrs=round(sum(total_hrs)))

@app.route('/job/edit/<value>')
def edit(value):
    user = User(session['username'], _id=session['user_id'])
    return render_template('user/edit.html', form=user.get_by_row_id(str(value)))

@app.route('/delete/<row>')
@login_required
def delete(row):
    user = User(session['username'], _id=session['user_id'])
    user.delete_row(row)
    return redirect(url_for('history'))

@app.route('/admin')
@login_required
def admin_login():
    session['username'] = 'admin'
    return redirect(url_for('history'))

@app.route('/user')
@login_required
def user_login():
    session['username'] = session['session_name']
    return redirect(url_for('history'))



@app.route('/update/<row>')
@login_required
def update(row):
    pass
