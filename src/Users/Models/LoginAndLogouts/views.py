##############################################################################
# Author: Egbie
##############################################################################

# ADD BLUE PRINTS HERE

@app.route('/admin')
@login_required
def admin_login_redirect():
    """Allows the user to redirect to history page whenever the user
       clicks their admin link.
    """
    session['username'] = 'admin'
    return redirect(url_for('history'))

@app.route('/user')
@login_required
def user_login_redirect():
    """Allows the user to redirect to history page whenever the user
       clicks their user link name.
    """
    session['username'] = session['session_name']
    return redirect(url_for('history'))

@app.route('/', methods=('GET', 'POST'))
@app.route('/login', methods=('GET', 'POST'))
def login():
    """Allows the user entry into the login applicaton"""
    form = LoginForm()
    return login_user(form=form,
                      session_name='username',
                      redirect_link='home',
                      template='forms/LoginRegistrationForm/login.html',
                      index='home')

@app.route('/logout')
@login_required
def logout():
    """log the user out of the application"""
    if session.get('admin', None):
        session.pop('admin')
    session.pop('username')
    session.pop('user_id')
    session.pop('session_name')
    return (redirect(url_for('login')))
