#####################################################################
# Author = Egbie Uku
#####################################################################

from src.utilities.converter import month_to_str

def is_leap_year(year):
    """Determine whether a year is a leap year."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def check_day(day):
    """Verifies whether the day entered by the user is an
    actually day.
    """
    days = {'mon': 'Monday',    'tue' : 'Tuesday',
           'wed' : 'Wednesday', 'thu' : 'Thursday',
               'fri' : 'Friday',    'sat' : 'Saturday',  'sun' : 'Sunday'}
    return days.get(str(day[0:3]).lower())

def check_date(date):
    """check_date(str) -> return(tuple)

    Takes a date and checks :
       - if the date is in the format  YYYY-MM-DD.
       - whether the month is between 1-12.
       - whether the days in the month April, June, September and November are 30 days.
       -  whether they are 28 days in February and 29 days if it is a leap year.
       - And finally checks whether they the rest of the months that are not February,
         April, June, September and November has 31 days.

     :parameters:
       - date: The date to check.
       - returns: A tuple consisting of two elements. If the date is correct
                  the first and second element which consists of the boolean value
                  True is returned to the user.
                  Otherwise returns two parts, where the first element
                  is False and the second element is an error message.

    >>> check_date(2016-02-29)
    >>> (False, 'They can only be 28 days in February since this year is  not a leap year.')
    >>>
    >>> check_date('2000-02-30)
    (False, 'They can only be 29 days in February since this year is a leap year.')
    >>>
    >>> check_date('2016-04-31')
    (False, 'check month, April as it has only 30 days!!')
    >>>
    >>> check_date('2016-04/31')
    >>> (False, 'replace the delimeter with "-" e.g. YYYY-MM-DD')
    >>>
    >>> check_date('2016-04-1')
    (False, 'incorrect date format try YYYY-MM-DD')
    >>>
    >>> check_date('2016-13-31')
    (False, 'month must be in the format of MM and between 1-12')
    >>.
    >>> check_date(''20167-13-31')
    (False, 'incorrect date format try YYYY-MM-DD')
    """
    if date != None:
        if len(date) == 10 :
             if '-' in date and date.count('-') == 2: # ensures that date
                 year, month, day = date.split('-')
                 if year.isdigit() and len(year) == 4:
                     if month.isdigit() and len(month) == 2 and  0 < int(month) <= 12:
                        if day.isdigit() and len(day) == 2:
                            thirty_days = [4, 6, 9, 11] # April(4), June(6), september(9) and November(11) months with 30 days
                            day, month = int(day), int(month)
                            if month == 2:  # check whether the month is feb and whether is a leap year
                                if is_leap_year(int(year)):
                                    if 1 <= day <= 29:
                                        return True, True
                                    return False, 'They can only be 29 days in February since this \
                                                   year {} is a leap year.'.format(year)
                                elif not is_leap_year(int(year)):
                                     if 1 <= day <= 29:
                                        return True, True
                                     return False, 'There can only be 28 days in February since this is not a leap year!!'
                            elif month in thirty_days:
                                    if 1 <= day <= 30:
                                        return True, True
                                    return False, 'check month, ' + month_to_str(month) + ' as it has only 30 days!!'
                            elif month not in thirty_days and month != 2:
                                    if 1 <= day <= 31:
                                        return True, True
                                    return False, 'check month ' + month_to_str(month) +' as it has only 31 days.'
                        return False,'day must be in the format of DD'
                     return False, 'month must be in the format of MM and between 1-12'
                 return False, 'year must be YYYY'
             return False, 'replace the delimeter with "-" e.g. YYYY-MM-DD'
        return False, 'incorrect date format try YYYY-MM-DD'
    return False, 'date cannot be None'
