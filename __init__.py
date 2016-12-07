from flask import Flask
from os import urandom

app = Flask(__name__)
app.secret_key = 'apple' #urandom(70)

from src.users import views
