#####################################################################
# Author = Egbie Uku
# Registration Class
#####################################################################

import uuid
from src.Users.Models.Databases.database import DataBase as db
from src.utilities.password_hasher import create_passwd_hash, check_passwd_hash
import time

class Registration(object):
    """Registration(class)
    Allows the user to register their details.
    """
    def __init__(self, email, password, registration_date=None, _id=None):
        self.email = email
        self.password = password
        self.registration_id = uuid.uuid4().hex if _id is None else _id
        self.registration_date = registration_date

    def _is_user_name_unique(self, email):
        """check whether the username is unique"""
        if db.find_one('login_credentials', {'username': self.email}):
           return False
        return True

    def register(self):
        """register the user
        Returns False if users details was not registered correctly.
        True if registration it was.
        """

        if not self._is_user_name_unique(self.email):
            return False
        self.password = create_passwd_hash(self.password) # hash password
        self._save()
        return True

    def _save(self):
        """Saves the registration details to the database in json format"""
        db.insert_one(collection='user_credentials', data=self._get_json())

    def _get_json(self):
        """Get the details of the registration in the form of a json format """
        return {'email'            : self.email,
                'password'         : self.password,
                'registration_date': time.strftime("%d/%m/%Y"),
                'registration_id'  : self.registration_id}
