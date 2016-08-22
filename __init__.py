from flask import Flask
from src.models.records import Records
from src.models.users import User
from src.models.utils import *
from src.users.models import Login, Registration
from src.users.form import LoginForm, RegisterForm
from src.models.database import DataBase


DataBase.initialize()
app = Flask(__name__)
