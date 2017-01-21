###############################################################################
# Author : Egbie
###############################################################################

import uuid
#from src.Users.Models.Databases.database import DataBase

class Cache(object):
    """Cache(class)

    The class stores the total amount of money
    earned for either the active or non-active jobs.

    This means if the users are viewing the
    job history or active jobs but no update
    is made in either one, the total amount of
    money accumulated for each one is
    returned from the cache instead
    of the database.
    """
    def __init__(self):
        self.cache = {}

    def save_to_cache(self, amount, active_jobs=False):
        if active_jobs:
            self.cache['active_jobs'] = amount
        else:
            self.cache['worked_jobs'] = amount

    def clear_cache(self):
        self.cache = []
        
