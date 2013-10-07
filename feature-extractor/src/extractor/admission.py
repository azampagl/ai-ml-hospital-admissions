"""
The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.4
@copyright 2013 - Present Aaron Zampaglione
"""
from datetime import datetime, timedelta

class Admission():
    """
    Admission class for hospital admissions.

    This class is responsible for parsing and normalizing raw admission data from hospitals.
    """

    # The number of periods (shifts) per day.  This is used to normalize the actual hour of admission.
    HOURS_PER_PERIOD = 4

    @staticmethod
    def createFromRaw(row):
        """
        Creates an admission object from raw admission data (e.g. rows in a csv file).
        
        Key arguments:
        row -- The raw admission data (row).
        """
        # Find the arrival date, arrival time, and the time admitted to the ER (transfer time).
        arrivalDate = [int(x) for x in row[1].split('/')]
        arrivalTime = datetime.strptime(row[2].zfill(4), '%H%M')
        transferTime = datetime.strptime(row[4].zfill(4), '%H%M')
        
        time = datetime(arrivalDate[2], arrivalDate[0], arrivalDate[1])
        # Add the hours, which is normalized by the number of hours in a period.
        time += timedelta(hours=transferTime.hour / Admission.HOURS_PER_PERIOD)
        
        # If the transfer time was earlier, than it must be the next day.
        if (transferTime < arrivalTime):
            time += timedelta(days=1)
        
        return Admission(time)

    @staticmethod
    def createFromKey(key):
        """
        Reconstructs an Admission object from an admission key.
        
        Key arguments:
        key -- The admission key.
        """
        return Admission(datetime.strptime(key, '%Y%m%d%H'))

    def __init__(self, time):
        """
        Creates the admission object and sets the time.
        
        Key arguments:
        time -- The time of admission.
        """
        self.time = time

    def key(self):
        """
        Returns the admission time as a string.  This should be used as the 
        key for an admission dictionary.
        
        Key arguments:
        row -- The raw admission data (row).
        """
        return self.time.strftime('%Y%m%d%H')