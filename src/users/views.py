from src.users.form import RegisterForm, LoginForm, AdminForm
from job_diary import app
from flask import render_template
from user_form_helpers import login_helper, register_helper


# use the _login_helper to log the user in
@app.route('/login', methods=('GET', 'POST'))
def login():
    """Allows the user entry to the login applicaton"""

    error = 'Incorrect username and password'
    url   = 'user/login.html'
    return login_helper(LoginForm, error, 'username', 'success', url)

# use the login helper to help assist the user in logging into admin console
@app.route('/admin', methods=('GET', 'POST'))
def admin():
    """Allows the user entry as admin"""

    error = 'Incorrect username your ip will be logged'
    url   = 'user/admin_login.html'
    return login_helper(AdminForm, error, 'admin', 'success', url)

@app.route('/admin/register', methods=('GET', 'POST'))
def admin_register():
    return register_helper(AdminForm, 'Incorrect admin name', 'user/admin_login.html', 'success')

@app.route('/register', methods=('GET', 'POST'))
def user_register():
    return register_helper(RegisterForm, 'username must be unique', 'user/registration.html', 'success')

@app.route('/success', methods=('GET', 'POST'))
def success():
    return render_template('user/entry_page.html')
