"""
See class comments.

The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2013 - Present Aaron Zampaglione
"""
 
class Node():
    """
    """
    
    def __init__(self):
        """
        """
        self.feature = None
        self.hyperplane = None
        self.left = None
        self.right = None
        self.threshold = None
        self.index = 0
    
    def __str__(self):
        """
        """
        return  "ID:\t" + str(id(self)) + "\n" \
                "Feature:\t" + str(self.feature) + "\n" \
                "Threshold:\t" + str(self.threshold) + "\n" \
                "Hyperplane:\t" + str(self.hyperplane.coefficients) + "\n"