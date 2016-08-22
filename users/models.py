from job_diary.models.database import DataBase as db
import bcrypt

class Login(object):"
    """Login(class) -> Checks whether the user registration is valid.
    If not returns the appropriate response.
    """
    def __init__(self, full_name, email, password, is_login=False):
        self.full_name = full_name
        self.password  = password
        self.email     = email
        self.is_login  = is_login

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
            self.is_login = True
            # update the login database by calling _update
            return True
        return False

    def _update(self):
        # change the is_login to true
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
            # means the users with does details already exists
            return False
        else:

            # Takes the users name, email and the hashed password and stores in database
            salt = bcrypt.gensalt(log_rounds=14)
            hash_password = bcrypt.hashpw(self.password, salt)
            user_details = RegistrationForm(self.full_name, email, hash_password)
            user_details.save()
            # redirect the user to the entry to the login page

    def save(self):
        db.insert(collection='login_details', self.json())

    def get_json():
        return {'full_name': self.full_name,
                'email'    : self.email
                'password' : self.password
                'is_login' : True}
