"""
The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.4
@copyright 2013 - Present Aaron Zampaglione
"""
from admission import Admission
from datetime import datetime, timedelta

class Extractor():
    """
    Extracts features from historical hospital admission data.
    """
    
    # The maximum number of weeks the extractor will look back to find a feature.
    MAX_WEEK_LOOK_BACK = 54
    
    @staticmethod
    def feature1(admissions, admission):
        """
        Finds the number of admissions 52 weeks ago.
        
        Key arguments:
        admissions  -- A dictionary of admissions.
        admission   -- The admission to find the feature for.
        """
        # Find the admission time 52 weeks ago.
        featureKey = Admission(admission.time - timedelta(weeks=52)).key()
        
        # Make sure we have records for this feature.
        if (admissions.has_key(featureKey)):
            return admissions[featureKey]
        
        return None

    @staticmethod
    def feature2(admissions, admission): 
        """
        Finds the average number of admission 52 weeks ago, the 2 previous weeks,
        and the 2 following weeks.
        
        Key arguments:
        admissions  -- A dictionary of admissions.
        admission   -- The admission to find the feature for.
        """      
        # List of feature keys to search.
        featureKeys = []
        
        # Find the admission time 52 weeks ago.
        featureKeys.append(Admission(admission.time - timedelta(weeks=50)).key())
        # Find the admission time 1 week ago.
        featureKeys.append(Admission(admission.time - timedelta(weeks=51)).key())
        # Find the admission time 2 weeks ago.
        featureKeys.append(Admission(admission.time - timedelta(weeks=52)).key())
        # Find the admission time 1 week in advance.
        featureKeys.append(Admission(admission.time - timedelta(weeks=53)).key())
        # Find the admission time 2 weeks in advance.
        featureKeys.append(Admission(admission.time - timedelta(weeks=54)).key())
        
        # Store all the feature values.
        featureValues = []
        for featureKey in featureKeys:
            # Make sure we have records for this feature.
            if (admissions.has_key(featureKey)):
                featureValues.append(admissions[featureKey])
            else:
                return None
        
        return sum(featureValues) / 5.0

    @staticmethod
    def feature3(admissions, admission):
        """
        Finds the number of admissions 365 days ago.
        
        Key arguments:
        admissions  -- A dictionary of admissions.
        admission   -- The admission to find the feature for.
        """
        # Find the admission time 365 days ago.
        featureKey = Admission(admission.time - timedelta(days=365)).key()
        
        # Make sure we have records for this feature.
        if (admissions.has_key(featureKey)):
            return admissions[featureKey]
        
        return None

    @staticmethod
    def feature4(admissions, admission):
        """
        Finds the average number of admissions over the past 3 weeks.
        
        Key arguments:
        admissions  -- A dictionary of admissions.
        admission   -- The admission to find the feature for.
        """  
        # List of feature keys to search.
        featureKeys = []
        
        # Find the admission time 1 week ago.
        featureKeys.append(Admission(admission.time - timedelta(weeks=1)).key())
        # Find the admission time 2 weeks ago.
        featureKeys.append(Admission(admission.time - timedelta(weeks=2)).key())
        # Find the admission time 3 weeks ago.
        featureKeys.append(Admission(admission.time - timedelta(weeks=3)).key())
        
        # Store all the feature values.
        featureValues = []
        for featureKey in featureKeys:
            # Make sure we have records for this feature.
            if (admissions.has_key(featureKey)):
                featureValues.append(admissions[featureKey])
            else:
                return None
        
        return sum(featureValues) / 3.0

    @staticmethod
    def feature5(admissions, admission):
        """
        Finds the weekly rate of change for admissions.
        
        Key arguments:
        admissions  -- A dictionary of admissions.
        admission   -- The admission to find the feature for.
        """ 
        # List of feature keys to search.
        featureKeys = []
        
        # Find the admission time 1 week ago.
        featureKeys.append(Admission(admission.time - timedelta(weeks=1)).key())
        # Find the admission time 2 weeks ago.
        featureKeys.append(Admission(admission.time - timedelta(weeks=2)).key())
        
        # Store all the feature values.
        featureValues = []
        for featureKey in featureKeys:
            # Make sure we have records for this feature.
            if (admissions.has_key(featureKey)):
                featureValues.append(admissions[featureKey])
            else:
                return None
        
        # Determine the slope, which is just the difference between the two values.
        return featureValues[0] - featureValues[1]

    @staticmethod
    def feature6(admissions, admission):
        """
        Finds the yearly rate of change for admissions.
        
        Key arguments:
        admissions  -- A dictionary of admissions.
        admission   -- The admission to find the feature for.
        """
        # List of feature keys to search.
        featureKeys = []
        
        # Find the admission time 1 week ago.
        featureKeys.append(Admission(admission.time - timedelta(weeks=1)).key())
        # Find the admission time 53 weeks ago.
        featureKeys.append(Admission(admission.time - timedelta(weeks=53)).key())
        
        # Store all the feature values.
        featureValues = []
        for featureKey in featureKeys:
            # Make sure we have records for this feature.
            if (admissions.has_key(featureKey)):
                featureValues.append(admissions[featureKey])
            else:
                return None
        
        # Find the slope, which is the difference between the two values.
        return (featureValues[0] - featureValues[1])

    @staticmethod
    def features(admissions, key):
        """
        Returns a set of features for an admission key.
        
        If any of the features could not be extracted, this returns
        None.
        
        Key arguments:
        admissions  -- A dictionary of admissions.
        admission   -- The admission to find the feature for.
        """        
        # Find the time of admission based on the key.
        admission = Admission.createFromKey(key)
        
        # Find all the features for this one entry.
        features = [
            Extractor.feature1(admissions, admission), 
            Extractor.feature2(admissions, admission), 
            Extractor.feature3(admissions, admission), 
            Extractor.feature4(admissions, admission), 
            Extractor.feature5(admissions, admission), 
            Extractor.feature6(admissions, admission), 
        ]
        
        # Return None if we were unable to get any of the features.
        return None if None in features else features