from flask import Flask
from src.models.database import DataBase
from src.models.records import Records
from src.models.users import User
from src.models.utils import *
from src.users.models import Login, Registration
from src.users import form

app = Flask(__name__)
db  = DataBase()
db.initialize()
