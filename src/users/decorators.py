from functools import wraps
from flask import session, request, redirect, url_for, abort


def login_required(func):
    """
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session.get('username') is None:
            return redirect(url_for('login', next=request.url))
        return func(*args, **kwargs)
    return decorated_function

def admin_required(func):
    """
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session.get('admin') is None:
            return redirect(url_for('login', next=request.url))
        return func(*args, **kwargs)
    return decorated_function
