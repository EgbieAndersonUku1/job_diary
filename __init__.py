from flask import Flask
from os import urandom

app = Flask(__name__)

# app.secret_key = apple is for testing purpose. Uncomment the first line
# for a more secure key and then comment the second line.

# IMPORT THE BLUEPRINT MODULES HERE AND REGISTER THEM HERE.
# app.secret_key = urandom(70)
app.secret_key = 'apple'#urandom(70)

from src.Users import views
from src.Users.Models.Registrations.views import user_registration
from src.Users.Models.LoginAndLogouts.views (url_admin_redirect,
                                             url_login_redirect,
                                             login_user,
                                             logout_user)
from src.Users.Forms.views import register_questions, retreive_password, search_page
from src.Users.Jobs.views import (editor, history, curr_jobs, job_info,
                                 resetor, deletor, permalink, job_entry)

app.register_blueprint(register_questions)
app.register_blueprint(retreive_password)
app.register_blueprint(search_page)
app.register_blueprint(editor)
app.register_blueprint(history)
app.register_blueprint(curr_jobs)
app.register_blueprint(job_info)
app.register_blueprint(resetor)
app.register_blueprint(deletor)
app.register_blueprint(permalink)
app.register_blueprint(job_entry)
app.register_blueprint(user_registration)
app.register_blueprint(url_admin_redirect)
app.register_blueprint(user_login_redirect)
app.register_blueprint(login_user)
app.register_blueprint(logout_user)
