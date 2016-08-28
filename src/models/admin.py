from src.users.models import Login, Registration
from src.models.database import DataBase


# AS AN ADMIN YOU BE ABLE TO SEE THE PEOPLE HOW MANY PEOPLE ARE LOGGED IN
# DELETE USERS ACCOUNT
# CREATE USER ACCOUNTS
# MAKE CHANGES TO THE WHOLE
# ADD A MESSAGE AND IT WOULD BE SEE BY ALL USERS

class Admin(DataBase):

    def _get_all(self, collections, query=None):
        """Return the total number of users that have an account"""
        return self.get_count(collections=collections, query=query)

    def get_all_users_num(self):
        """Return the total number of users who have an account"""
        return self._get_all(collections='user_credentials')

    def get_num_of_logged_in_users(self):
        """return the total of number of people who are currently logged in"""
        return self._get_all(collections='login_credentials', query={'is_logged_in': 'True'})

    def get_by_email(self, email):
        """Return the details of a single user via email"""
        data = self.find_one(collections='user_credentials', query={'email': email})
        if data:
            return Registration(**data)

    def create_account(self, full_name, email, password):
        pass

    def delete_account(self, email):
        pass

    def de_activate_account(self, email):
        pass

    def re_activate_account(self, email):
        pass

    
