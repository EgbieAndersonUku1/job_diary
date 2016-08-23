from src.users.form import RegisterForm, LoginForm
from src.users.models import Login, Registration
from job_diary import app
from flask import url_for, session, redirect, request

@app.route('/login', methods=('GET', 'POST'))
def login():
    """Allows the user entry to the applicaton"""
    form  = RegisterForm()
    error = ''

    if form.validate_on_submit():
        user = Login(form.username.data, form.password.data)
        if user.is_credentials_ok():
            session['username'] = user.username
            return redirect(url_for('success'))
        else:
            error = 'Incorrect username and password'
    error = 'Incorrect username and password'
    return render_template('/user/login.html', form=form, error=error)

@app.route('/register', methods=('GET', 'POST'))
def register():
    """Register the users details to the application"""

    form  = RegisterForm()
    error = " "

    # if form validates attempt to register users details.
    # if registration is successful meaning username is unique log user in.
    if form.validate_on_submit():
        user = Registration(form.full_name.data, form.email.data, form.password.data)

        # attempt to register the user
        if user.register():
            user = Login(user.username, user.password) # log the user into the application
            user.save()                                # save username and encrypted password to the database
            session['username'] = user.username
            return redirect(url_for('success'))
        else:
            error = 'The username must be unique'
            return render_template('/users/registration.html', form=form, error=error)

    error = 'Check your details and try again.'
    return render_template('/users/registration.html', form=form, error=error)


app.route('/entry_page')
def success():
    return render_template('/user/entry_page.html')
