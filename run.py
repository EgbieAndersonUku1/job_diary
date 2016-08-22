import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask_script import Manager, Server
from job_diary import app



manager = Manager(app)
manager.add_command('runserver', Server(
                     use_debugger=True,
                     use_reloader=True,
                    ))


if __name__ == '__main__':
    manager.run()
