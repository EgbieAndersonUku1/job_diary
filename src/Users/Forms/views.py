from flask import render_template, url_for, Blueprint, redirect, session
from src.Users.decorators import login_required, admin_required

search_page = Blueprint('search_page', __name__)
register_questions = Blueprint('register_questions', __name__)
retreive_password = Blueprint('password_retrieval', __name__)

SEARCH_FORM_JOBS = ''

@search_page.route('/search', methods=('GET', 'POST'))
@login_required
def search():
    """Search form that allows the user to search the form based on the job attributes"""

    # FIX THE CODE REQUIRING THE RADIO BUTTONS
    #title  = request.form.get('jobInfo')
    form = SearchForm()
    error = ''
    if request.method == 'POST':
        if form.validate_on_submit:

            search_form = ValidateSearchForm(form)
            jobs = search_form.get_data()
            if jobs:
                global SEARCH_FORM_JOBS
                SEARCH_FORM_JOBS = jobs
                return redirect(url_for('perma_link'))
        error = 'No records find by that entry'
        return render_template('forms/SearchPageForm/search_page.html', form=form, error=error)
    return render_template('forms/SearchPageForm/search_page.html', form=form)

@register_questions.route('/secret/questions', methods=('GET', 'POST'))
def register_secret_questions_answers():

    form = ForgottenPasswordForm()
    if form.validate_on_submit():
        user = User(session['username'], _id=session['user_id'])
        user.save_secret_answers(form, session['username'])
        return redirect('login')
    return render_template('forms/SecretQuestions/secret_questions_registration.html',
                           form=form,
                           username=session['username'])

@retreive_password.route('/secret/questions/answers', methods=('GET', 'POST'))
def forgotten_password():
    """
    """
    form  = ForgottenPasswordForm()
    error = ''
    if form.validate_on_submit():
        user_answers = ValidiateSecretQuestions(form)
        if user_answers.validate_answers():
            session['username'] = form.username.data.lower()
            return redirect(url_for('new_password'))
        error = 'The user was not found'
    return render_template('forms/SecretQuestions/secret_questions_answers.html', form=form, error=error)

@app.route('/newpassword', methods=('GET', 'POST'))
def new_password():
    """
    """
    form = NewPasswordForm()
    if form.validate_on_submit():
        user = User(session['username'])
        hash_password = create_passwd_hash(str(form.password.data))
        user.update_password(session['username'], hash_password)
        user_id = user.get_user_id(session['username'])
        session['user_id'] = user_id
        session['session_name'] = session['username']
        return redirect('login')
    return render_template('forms/NewPasswordsForm/new_password_form.html', form=form)
