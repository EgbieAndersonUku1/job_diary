###############################################################################
# Author : Egbie
#
# TO BE USED IN THE PERMALINKS, ACTIVE AND JOB HISTORY HTML PAGE.
# BEFORE THIS IMPLEMENTATION WHENEVER THE TOTAL AMOUNT AND TOTAL HRS
# WERE TO BE CALCULATED FOR EITHER THE ACTIVE, PERMALINKS OR WORKED JOBS PAGE.
# IT WOULD BE DONE BY FIRST OBTAINING THE NECESSARY JOBS WHICH IS
# COULD EITHER ACTIVE OR WORKED JOBS. THEN THE ENTIRE JOBS WAS THEN LOOPED
#  IN THE JOBS HELPER PAGE WHERE THE THE TOTAL PAY AND TOTAL HOURS WERE OBTAINED.
#  THEN IN ORDER TO DISPLAY THE RESULT TO THE USER IT WAS THEN LOOPED AGAIN
# AND THE RESULT DISPLAYED IN THE APPROPRIATE ROWS AND COLUMNS.

# THIS MAKES THE ALGORITHM USED O(N^2) INSTEAD OF 0(N). NOW BY USING THE TOTALAMOUNT
# CLASS TO CALCULATING THE TOTAL HRS AND TOTAL PAY AT THE SAME TIME THE RESULTS
# ARE BEING DISPLAYED, THE THE RESULTING ALGORITHM NOW BECOMES 0(N)
###############################################################################

from src.utilities.converter import units_to_hours

class TotalAmount(object):
    """returns the total amount of money for the jobs"""

    total = []
    hrs = []

    @classmethod
    def store_hrs(cls, hrs):
        cls.hrs.append(float(hrs))
        return ''

    @classmethod
    def get_hrs(cls):
        return units_to_hours(sum(cls.hrs))

    @classmethod
    def store_val(cls, value):
        """Stores the values """
        cls.total.append(float(value))
        return ''

    @classmethod
    def get_total(cls):
        """return the total amount of money"""
        return round(sum(cls.total), 2)

    @classmethod
    def clear_all(cls):
        """clears the hours and amount field"""
        cls.total, cls.hrs = [], []
        return ''
