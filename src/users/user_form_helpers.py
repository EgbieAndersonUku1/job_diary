from flask import render_template, redirect, session, url_for
from src.users.models import Login, Registration

def login_helper(form_obj, msg, *args):
    """
    Helper function that assists the user entry to the applicaton
    form_obj(func) : Takes either been a login form func or admin form func and renders it
    msg            : An error message or message to display
    template       : The template to display
    """

    form          = form_obj()
    session_name  = args[0]     # the name for the session
    redirect_url  = args[1]     # the redirect url for any successful login
    template      = args[2]     # the url for the template to render

    if form.validate_on_submit():
        user = Login(form.username.data, form.password.data)
        if user.is_credentials_ok():
            session[session_name] = user.username
            return redirect(url_for(redirect_url))
    error = msg
    return render_template(template, form=form, error=error)

def register_helper(obj, msg, template, url_redirection_name):
    """
    Helper function assists the users in registrating their details.

    obj     : either a normal registration or admin registration obj
    msg     : msg to display to the user
    template: The template to use
    url_redirection_name: The page to redirect to after success
    """
    form  = obj()

    # if form validates attempt to register users details.
    # if registration is successful meaning username is unique log user in.
    if form.validate_on_submit():
        user = Registration(form.full_name.data.title(), form.email.data, form.password.data)

        # attempt to register the user
        if user.register():
            user = Login(user.email, user.password, True) # log the user into the application
            user.save()                                   # save username and encrypted password to the database
            session['username'] = user.username
            return redirect(url_for(url_redirection_name))
        else:
            error = msg
            return render_template(template, form=form, error=error)
    error = 'Check your details and try again.'
    return render_template(template, form=form, error=error)
