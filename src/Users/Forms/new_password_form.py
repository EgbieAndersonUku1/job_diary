from flask_wtf import Form
from wtforms import validators, StringField, PasswordField

class NewPasswordForm(Form):
    """NewPasswordForm(class)
    Allow the user to enter a new password for their current account.
    """
    password = PasswordField('New password',
                           [validators.Required(),
                           validators.Length(min=4, max=80),
                           validators.EqualTo('confirm', message='password does not match')])
    confirm = PasswordField('Repeat password')
