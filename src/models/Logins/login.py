from src.models.Databases.database import DataBase as db
from datetime import datetime
from uuid import uuid4
from src.utilities.common import create_passwd_hash, check_passwd_hash
import bcrypt

class Login(object):
    """Login(class) -> Checks whether the user registration is valid.
    If not returns the appropriate response.
    """
    def __init__(self, username, password, _id=None,
                 is_admin=False, logged_in_time=datetime.utcnow()):

        self.username  = username
        self.password  = password
        self._id  = uuid4().hex if _id is None else _id
        self.is_admin  = is_admin
        self.logged_in_time = logged_in_time

    def _get_user_login_details(self):
        """func : _get_user_login_details(None) -> return(obj or None)
        Helper function: Checks whether the user details
        exists returns obj or False otherwise.
        """
        login_data = db.find_one(collections='login_credentials',
                                query={'username': self.username})
        return False if not login_data else Login(**login_data)

    def is_credentials_ok(self):
        """func : check_user_details(None) -> return(None)
        Checks whether the users details are correct. Returns False
        or a login object.
        """
        login_obj = self._get_user_login_details()
        if not login_obj:
           return False # users details does not exist
        elif check_passwd_hash(self.password, login_obj.password):
           return login_obj
        return False

    def save(self):
        """Saves the form to the database in json format"""
        db.insert_one(collection='login_credentials', data=self._json())

    def _json(self):
        """returns a json representation of the form"""
        return {'username'      : self.username,
                'password'      : self.password,
                'is_admin'      : self.is_admin,
                '_id'           : self._id,
                'logged_in_time': self.logged_in_time }
