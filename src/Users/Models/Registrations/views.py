###############################################################################
# Author; Egbie
###############################################################################

# ADD BLUEPRINT HERE

@app.route('/register', methods=('GET', 'POST'))
def user_register():
    """Register the user to the application"""
    form = RegisterForm()
    return register_user(form=form,
                         error='username must be unique',
                         template='forms/LoginRegistrationForm/registration.html',
                         redirect_link='home')
