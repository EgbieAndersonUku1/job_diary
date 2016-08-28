from flask import Flask

app = Flask(__name__)
app.secret_key = 'This is a super secret key'

from src.users import views
