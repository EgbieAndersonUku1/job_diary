from flask import render_template, redirect, session, url_for, request, abort
from src.users.models import Login, Registration

def login_helper(form_obj, *args):
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


    #return login_helper(LoginForm, 'username', 'success', 'user/login.html', 'index', False, error)

    # if we can found a session it means that the user is already logged in
    if session.get(session_name, None):
        return redirect(url_for(index_page))

    elif request.method == 'GET':
        return render_template(template, form=form, error='')
    else:

        if form.validate_on_submit():
            if admin:
                user = Login(form.admin_name.data, form.password.data)
            else:
                user = Login(form.username.data, form.password.data)
                login_obj  = user.is_credentials_ok()
            if login_obj:

                session[session_name] = login_obj.username
                session['user_id'] = login_obj._id
                return redirect(url_for(redirect_link))

            elif admin:
                abort(403) # ABORT SINCE OBVIOUSLY THAT USER IS NOT ADMIN.
                           # SOME FUNCTIONALITY TO LOG IP ADDRESSES
            session[session_name] = user.username
            session['user_id'] = user._id
        return render_template(template, form=form, error='Incorrect username and password')


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

    if request.method == 'GET':
        return render_template(template, form=form, error=error)

    if request.method == 'GET' and request.args.get('next'):
        session['next'] = request.args.get('next')

    # if form validates attempt to register users details.
    # if registration is successful meaning username is unique log user in.
    if form.validate_on_submit():
        user = Registration(form.full_name.data.title(), form.email.data, form.password.data)

        # attempt to register the user
        if user.register():
            user = Login(user.email, user.password, True) # log the user into the application
            user.save()                                   # save username and encrypted password to the database
            session['username'] = user.username
            session['user_id'] = user._id
            if 'next' in session:
                return session.pop('next')
            else:
                return redirect(url_for(redirect_link))
        else:
            error = msg
            return render_template(template, form=form, error=error)
