from flask import Flask
from job_diary.models.database import DataBase
from job_diary.models.records import Records
from job_diary.models.users import User


app = Flask(__name__)
db  = DataBase()
db.initialize()
