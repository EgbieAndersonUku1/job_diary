from flask import Flask
from os import urandom

app = Flask(__name__)

# app.secret_key = apple is for testing purpose. Uncomment the first line 
# for a more secure key and then comment the second line.

# app.secret_key = urandom(70)
app.secret_key = 'apple'#urandom(70) 

from src.users import views
