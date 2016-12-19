###############################################################################
# author : Egbie Uku
#
# Enables the user to make changes to their account.
# For example change the password, delete the account, etc
###############################################################################

from src.models.Records.record import Records

class User(object):
    """User(class)
    Enables the user to make changes to their account.
    For example change the password, delete the account,
    etc
    """
    def __init__(self, username, _id):
        self.id = _id
        self.username = username

    def save_secret_answers(self, form, username):
        """save_secret_answers(obj) -> return(None)

        Stores the user secret answers and questions
        to the database.
        """
        Records.save_secret_answers(form, self.id, username)

    def validate_answers(self, form):
        """validate_answers(obj) -> return(bool)

        Validate the answers for for the secret
        answers and returns True if the answers
        are correct and False otherwise.

        :parameters
           - form: A form object containing the users
                   secret answers
        """
        return ValidiateSecretQuestions(form)

    def update_password(self, username, password):
        """update_password

        Updates the old password to the new password.
        """
        Records.update_password(username, password)

    def get_user_id(self, username):
        return Records.get_user_id(username)

    def de_activate_account(self):
        """alllows the person to delete their
        account along with all their data."""
        pass
