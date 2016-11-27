from flask import render_template, redirect, session, url_for, request, abort
from src.models.login import Login
from src.models.registration import Registration


def login_user(**kw):
    """
    Helper function: that assists the user entry to the applicaton

    @ key word params:
    form         : form object to render
    template     : The template to display
    session_name : The session name to be used with this session
    """
    
    # if we can found a session it means that the user is already logged in
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
                error = 'Incorrect username and password'
        return render_template(kw['template'], form=kw['form'], error=error)

def register_user(**kw):
    """
    Register the user to the application.

    @keyword parmas :
    obj     : either a normal registration or admin registration obj
    msg     : msg to display to the user
    template: The template to use
    redirect_link: The page to redirect to after success login
    """
    
    if request.method == 'GET':
        return render_template(kw['template'], form=kw['form'], error=kw['error'])
    if request.method == 'GET' and request.args.get('next'):
        session['next'] = request.args.get('next')

    # if form validates attempt to register users details.
    # if registration is successful meaning username is unique log user in.
    if kw['form'].validate_on_submit():
        user = Registration(kw['form'].email.data, kw['form'].password.data)
        if user.register():                         # attempt to register the user
            user = Login(user.email, user.password) # log the user into the application
            user.save()                             # save username and encrypted password to the database
            session['username'] = user.username     # encode the user details to a session cookier
            session['user_id']  = user._id
            session['session_name'] = user.username # holds the current user session name
            if 'next' in session:
                return redirect(session.pop('next'))
            return redirect(url_for(kw['redirect_link']))
    return render_template(kw['template'], form=kw['form'], error=kw['error'])
