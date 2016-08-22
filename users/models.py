
from job_diary.models.database import DataBase as db
from datetime import datetime
import time
import bcrypt

class Login(object):"
    """Login(class) -> Checks whether the user registration is valid.
    If not returns the appropriate response.
    """
    def __init__(self, full_name, email, password, is_logged_in=False):
        self.full_name = full_name
        self.password  = password
        self.email     = email
        self.is_logged_in   = is_logged_in
        self.logged_in_time = datetime.utcnow() # the time the user logged in

    def _get_user_login_details(self):
        """func : _get_user_login_details(None) -> return(obj or None)
        Helper function: Checks whether the user details returns obj or False
        otherwise.
        """
        login_data = db.find_one(collections='login_details', query={'email': self.email})
        if login_data:
            return Login(**login_data)

    def check_user_details(self):
        """func : check_user_details(None) -> return(None)
        Checks whether the users details are correct. Returns True if it is
        and False otherwise
        """
        login_obj = self.get_user_login_details()
        if bcrypt.hashpw(self.password, login_obj.password) == login_obj.password:
            self.is_logged_in = True # set the login to true
            return True              # users details check out
        return False                 # users details did not check out

    def _update(self):
        # change the is_logged_in to true
        # write the functionality here
        pass

class Registration(object):
    """Registration(class)
    Allows the user to register their details.
    """
    def __init__(self, full_name, email, password):
        self.full_name = full_name
        self.email = email
        self.password = password

    def does_user_exist(self):
        """Checks whether the user alreay exists with the database """

        if db.find_one(collections='login_details', query={'email': self.email}):
            return False # False means the users with does details already exists
        else:
            # Takes the users name, email and the hashed password and stores in database
            salt = bcrypt.gensalt(log_rounds=14)
            hash_password = bcrypt.hashpw(self.password, salt)
            user_details = RegistrationForm(self.full_name, email, hash_password)
            user_details.save()
            return True # True Means that everything was created smoothly

    def save(self):
        """Saves the registration details to the database"""
        db.insert(collection='login_details', self.json())

    def get_json():
        """Get the details of the registration in the form of a json format """
        return {'full_name'     : self.full_name,
                'email'         : self.email
                'password'      : self.password
                'is_logged_in'  : True,
                'registration date': time.strftime("%d/%m/%Y")}
