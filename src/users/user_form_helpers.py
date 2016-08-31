from flask import render_template, redirect, session, url_for, request
from src.users.models import Login, Registration

def login_helper(form_obj, msg, *args):
    """
    Helper function: that assists the user entry to the applicaton
    form_obj       : Takes either been a login form func or admin form func and renders it
    msg            : An error message or message to display
    template       : The template to display
    """

    form           = form_obj()
    session_name   = args[0]     # the name for the session
    redirect_link  = args[1]     # the redirect url for any successful login
    template       = args[2]     # the url for the template to render
    index_page     = args[3]
    admin          = args[4]
    error          = ''

    if session.get(session_name, None):
        return redirect(url_for(index_page))
    elif form.validate_on_submit():
        if admin:
            user = Login(form.admin_name.data, form.password.data)
        else:
            user = Login(form.username.data, form.password.data)
        if user.is_credentials_ok():
            session[session_name] = user.username
            return redirect(url_for(redirect_link))

    if request.method == 'GET':
        return render_template(template, form=form, error=error)
    else:
        error = msg
        # SOME FUNCTION THAT LOGGES IN IP ONLY IF THE USER IS ADMIN
        return render_template(template, form=form, error=error)

def register_helper(obj, msg, template, redirect_link):
    """
    Helper function assists the users in registrating their details.

    obj     : either a normal registration or admin registration obj
    msg     : msg to display to the user
    template: The template to use
    redirect_link: The page to redirect to after success login
    """
    form  = obj()
    error = ''

    # if form validates attempt to register users details.
    # if registration is successful meaning username is unique log user in.
    if form.validate_on_submit():
        user = Registration(form.full_name.data.title(), form.email.data, form.password.data)

        # attempt to register the user
        if user.register():
            user = Login(user.email, user.password, True) # log the user into the application
            user.save()                                   # save username and encrypted password to the database
            session['username'] = user.username
            return redirect(url_for(redirect_link))
        else:
            error = msg
            return render_template(template, form=form, error=error)
    if request.method == 'GET':
        return render_template(template, form=form, error=error)
    else:
        error = 'Check your details and try again.'
        return render_template(template, form=form, error=error)
