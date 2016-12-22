#####################################################################
# Author = Egbie Uku
#####################################################################

from functools import wraps
from flask import session, request, url_for, redirect

def _login_helper(func, user='username'):
    """helper function that adds additional help to the
    login required function and admin required function.
    The help comes in the form of checking whether the user
    is logged in as a user or as an admin.
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session.get(user) is None:
            return redirect(url_for('login', next=request.url))
        return func(*args, **kwargs)
    return decorated_function

def login_required(func):
    """check if the user is logged in"""
    return _login_helper(func)

def admin_required(func):
    """check if admin is logged in"""
    return _login_helper(func, user='admin')
