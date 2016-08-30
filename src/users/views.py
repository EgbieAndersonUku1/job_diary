from src.users.form import RegisterForm, LoginForm, AdminForm
from job_diary import app
from flask import render_template
from user_form_helpers import login_helper, register_helper

# use the _login_helper to log the user in
@app.route('/', methods=('GET', 'POST'))
@app.route('/login', methods=('GET', 'POST'))
def login():
    """Allows the user entry to the login applicaton"""
    error = 'Incorrect username and password'
    return login_helper(LoginForm, error, 'username', 'success', 'user/login.html')

# use the login helper to help assist the user in logging into admin console
@app.route('/admin/', methods=('GET', 'POST'))
@app.route('/admin/login', methods=('GET', 'POST'))
def admin():
    """Allows the user entry as admin"""

    error = 'Incorrect username your ip will be logged'
    return login_helper(AdminForm, error, 'admin', 'success', 'admin/admin_login.html')

# admin registration
@app.route('/admin/register', methods=('GET', 'POST'))
def admin_register():
    return register_helper(AdminForm, 'Incorrect admin name', 'admin/admin.html', 'success')

# user registration
@app.route('/register', methods=('GET', 'POST'))
def user_register():
    return register_helper(RegisterForm, 'username must be unique', 'user/registration.html', 'success')

@app.route('/success', methods=('GET', 'POST'))
def success():
    return render_template('user/entry_page.html')
