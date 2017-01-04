###############################################################################
# Author = Egbie Uku
###############################################################################

from flask import render_template, redirect, session, url_for, request, abort
from src.Users.Models.Logins.login import Login
from src.Users.Models.Registrations.registration import Registration

def login_user(**kw):
    """
    Helper function: that assists the user entry to the applicaton

    parameters:
        - form: form object to render.
        - template     : The template to display.
        - session_name : The session name to be used with this session.
    """
    msg = ''
    if session.get(kw['session_name'], None) != None:
        return redirect(url_for(kw['index']))
    if request.method == 'GET' and request.args.get('next'):
        session['next'] = request.args.get('next')
    elif request.method == 'GET':
        return render_template(kw['template'], form=kw['form'], error='')
    else:
        if kw['form'].validate_on_submit():
            user = Login(kw['form'].username.data, kw['form'].password.data)
            login_obj = user.is_credentials_ok()
            if login_obj:
                # encode the session with users details
                session[kw['session_name']] = login_obj.username
                session['user_id'] = login_obj._id
                session['session_name'] = login_obj.username
                if 'next' in session:
                    url = session.pop('next')
                    return redirect(url)
                return redirect(url_for(kw['redirect_link']))
            else:
                msg = 'Incorrect username and password'
        return render_template(kw['template'], form=kw['form'], error=msg)

def register_user(**kw):
    """
    Register the user to the application.

    :parameters
        - obj: either a normal registration or admin registration obj
        - msg: msg to display to the user
        - template: The template to use
        - redirect_link: The page to redirect to after success login
    """
    if request.method == 'GET':
        return render_template(kw['template'], form=kw['form'], error='')
    if request.method == 'GET' and request.args.get('next'):
        session['next'] = request.args.get('next')

    # if the form validates, attempt to register the users details.
    # If registration is successful meaning that username is unique and
    # the password is acceptable, log the user into the application.
    # Next create the cache system
    # Finally encode their details within a session.
    if kw['form'].validate_on_submit():
        user = Registration(kw['form'].email.data, kw['form'].password.data)
        if user.register():
            user = Login(user.email, user.password) # logs the user in.
            session['username'] = user.username
            session['user_id'] = user._id
            session['session_name'] = user.username
            cache = Cache(session['user_id']) # create the cache in db
            user.save()
            return redirect(url_for('register_secret_questions_answers'))
    return render_template(kw['template'], form=kw['form'], error=kw['error'])
