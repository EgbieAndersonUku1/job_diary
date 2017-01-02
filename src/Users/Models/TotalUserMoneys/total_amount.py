###############################################################################
# Author : Egbie
###############################################################################
from src.Users.user import User
from src.Users.Models.Databases.database import DataBase

class TotalAmount(object):

    def __init__(self, obj, instance):
        if not isinstance(instance, obj):
            raise ValueError('The instance does not belong to the class.')
        self.amount = []
        self._id = session['user_id']
        self.instance = instance

    def store(self, value):
        self.amount.append(float(value))
        return ''

    def get_total(self):
        return sum(self.amount)

    def get_cache(self, value):

        # if the value if false it means the
        # Cache was not updated so use the
        # value stored in the cache instead.
        if not self.instance.get_update():
            return self.instance.get_cache(value)
        user = User(session['username'], _id['session'])
        if value:
            return user.get_all_active_jobs()
        return self.user.get_wor
