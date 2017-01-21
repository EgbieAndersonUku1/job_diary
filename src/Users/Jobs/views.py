#########################################################################
# Author: Egbie
# ADD BLUE PRINTS HERE ALONG WITH APPROPRIATE MODULES FROM flask
########################################################################

from flask import render_template, redirect, url_for, Blueprint, request
from src.Users.decorators import login_required

editor = Blueprint('editor', __name__)
history = Blueprint('history', __name__)
curr_jobs = Blueprint('curr_jobs', __name__)
job_info = Blueprint('job_info', __name__)
resetor = Blueprint('restor', __name__)
deletor = Blueprint('deletor', __name__)
permalink = Blueprint('permalink', __name__)
job_entry = Blueprint('job_entry', __name__)

def _redirector(row_id, job_status, update=False):
    if job_status == 'unconfirmed':
         return redirect(url_for('history'))
    return redirect(url_for('info_page', row_id=row_id))

def _render_template(html_link, active=False, permalink_jobs=False):
    """_display(str, str) -> return(value)

    :parameters
        - html_link: The link of the page to render
        - active   : Whether the jobs are active e.g not worked yet.
        - returns  : Render object.

    Renders the jobs worked or not worked along with the hours and total pay.
    """
    jobs, user = get_jobs(active, permalink_jobs,User, session, curr_date)
    return render_template(html_link,
                           jobs=jobs,
                           translate=month_to_str, # total hrs expressed in units e.g 12.75
                           date=curr_date,
                           is_shift_over=is_shift_over,
                           converter=units_to_hours,
                           when_is_shift_starting=when_is_shift_starting,
                           is_shift_now=is_shift_now,
                           is_shift_confirmed=is_shift_confirmed,
                           user=user, len=len, total=TotalAmount)

@editor.route('/job/edit/<value>')
@login_required
def edit_job(value):
    """Allows the jobs to be edited"""
    user = User(session['username'], _id=session['user_id'])
    return render_template('forms/EditForm/edit_page.html', form=user.get_job_by_row_id(str(value)))

@history.route('/history/jobs', methods=('GET', 'POST'))
@login_required
def job_histories():
    """renders the entire job history active and none active"""
    return _render_template('forms/WorkedJobs/jobs_history.html')

@curr_jobs.route('/active/jobs', methods=('GET', 'POST'))
@login_required
def current_jobs():
    """renders the all jobs that are active (not worked)"""
    return _render_template('forms/CurrentJobs/current_jobs.html', True)

@job_info.route('/info/<row_id>')
@login_required
def job_info_page(row_id):
   """redirects the user to successful page entry after successful input"""
   user = User(session['username'],_id=session['user_id'])
   return render_template('forms/permalinks/perma_table.html', rows=user.get_job_by_row_id(row_id))

@resetor.route('/jobs/reset')
@login_required
def reset_job_page():
    """reset the value in the form for the application"""
    return redirect(url_for('job_entry.entry_page', row_ID=False))

@permalink.route('/search/permalinks/jobs')
def job_perma_link():
    """Displays the jobs retreived from the search function"""
    return _render_template("forms/permalinks/perma_link.html", permalink_jobs=SEARCH_FORM_JOBS)


@deletor.route('/delete/<row>')
@login_required
def delete_job_page(row):
    """deletes data from the a specific row"""
    user = User(session['username'], _id=session['user_id'])
    user.delete_job(row)
    return redirect(request.referrer)


@job_entry.route('/job/entry/<row_ID>', methods=('GET', 'POST'))
@login_required
def job_entry_page(row_ID):
    """entry_page(func)
    Retreives and process the users data. Also renders the user data
    from the entry job page.
    """
    start_date, end_date = curr_date, curr_date
    descr   = request.form.get('description', '')
    title   = request.form.get('job_title', '')
    day     = request.form.get('day', curr_day)
    loc     = request.form.get('location', '')
    hourly_rate = request.form.get('hourly_rate', '')
    start_date  = request.form.get('start_date', curr_date)
    end_date    = request.form.get('end_date', curr_date)
    start_hours = request.form.get('start_hours')
    start_mins  = request.form.get('start_mins')
    end_hours   = request.form.get('end_hours')
    end_mins    = request.form.get('end_mins')
    is_shift_confirmed = request.form.get('is_shift_confirmed')

    if request.method == 'GET':
        return render_template('forms/JobEntryForm/job_entry_page.html',
                                start_date=start_date,
                                end_date=end_date,
                                day=day,
                                job_title=title,
                                description=descr,
                                location=loc,
                                start_hours=start_hours,
                                start_mins=start_mins,
                                rate=hourly_rate,
                                end_hours=end_hours,
                                end_mins=end_mins,
                                errors='',
                                success='',
                                is_shift_confirmed=is_shift_confirmed)

    job_form = ValidateJobDetailsForm(title, descr, loc,
                                      hourly_rate, start_date,
                                      end_date, day,
                                      is_shift_confirmed,
                                      start_hours,
                                      start_mins, end_hours,
                                      end_mins)
    success, errors, job = job_form.verify_form()
    if success:
        # row_ID comes from the form so False is expressed as a unicode
        # instead of a boolean. This make the if-condition
        # if row_ID == False or not(row_ID) == False always equals True instead
        # of False.
        # By expressing it as str(row_ID) != 'False' it makes the if-statement
        # False when the string returned is not equal to the string False.
        if str(row_ID) != 'False': # means the row should be updated.
            msg, row_id = Evaluator.evaluate_and_save(job, curr_date, row_ID, True)
        else:
            msg, row_id = Evaluator.evaluate_and_save(job,curr_date)
        return redirector(row_id, msg)

    # Render the details already entered by the user.
    return render_template('forms/JobEntryForm/job_entry_page.html',
                           start_date=job.start_date,
                           end_date=job.end_date,
                           job_title=job.job_title,
                           description=job.description,
                           location=job.location,
                           start_hours=job.start_hours,
                           start_mins=job.start_mins,
                           end_hours=job.end_hours,
                           end_mins=job.end_mins,
                           day=job.day,
                           rate=job.rate,
                           errors=errors,
                           is_shift_confirmed=is_shift_confirmed)
