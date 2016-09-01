from src.users.form import RegisterForm, LoginForm, AdminRegisterForm, AdminLoginForm
from job_diary import app
from flask import render_template, session, redirect, url_for
from user_form_helpers import login_helper, register_helper

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

@app.route('/success', methods=('GET', 'POST'))
def success():
    return render_template('user/entry_page.html')


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
