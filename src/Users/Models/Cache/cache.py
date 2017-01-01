###############################################################################
# Author : Egbie
###############################################################################

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
    def __init__(self, updated=False):
        self._active_jobs_cache = None
        self._non_active_jobs_cache = None
        self._updated = updated # if true tells tha

    def get_update(self):
        """returns whether the cache was updated"""
        return self._updated

    def set_updated(self, status):
        self._updated = status

    def _get_active_job_cache(self):
        """returns the total amount of money a
        accumulated for active jobs.
        """
        return self._active_jobs_cache

    def _get_non_active_job_cache(self):
        """_get_non_active_job_cache(None) -> return(None)

        Returns the total amount of money
        accumulated for non-active jobs.
        """
        return self._non_active_jobs_cache

    def clear_caches(self):
        """clear_caches(None) -> return(None)

        Clears the caches for both active and
        non-active jobs.
        """
        self._active_jobs_cache = None
        self._non_active_jobs_cache = None

    def save_to_cache(self, value, save_to_active_cache=False):
        """save_to_cache(str, boolean(optional)) -> return(None)

        Save a values to the cache. If the flag save_to_active_cache
        is set to True stores saves the value to that active job cache or
        if set to False saves it to the non active jobs.
        """
        if save_to_active_cache:
            self._active_jobs_cache = value
            return ''
        self._non_active_jobs_cache = value
        return ''

    def get_cache(self, return_active_jobs=False):
        """get_cache(str) -> return()

        If active is set to False Returns
        all jobs that are active otherwise
        returns all non-active jobs (jobs that
        the user has already worked).
        """
        if return_active_jobs:
            return self._active_jobs_cache
        return self._non_active_jobs_cache
