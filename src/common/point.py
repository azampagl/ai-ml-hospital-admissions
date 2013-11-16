"""
The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2013 - Present Aaron Zampaglione
"""
from numpy import array, linalg
 
class Point():
    
    def __init__(self, features, solution = None):
        """
        """
        self.features = features
        self.solution = solution
        
        # Copy over the original features set.
        self.coordinates = list(features)
        # Append the solution to the end of the coodinates list.
        self.coordinates.append(solution)
        
        # Find the dimension of the point.
        self.dimension = len(self.coordinates)
    
    def __str__(self):
        """
        """
        return "(" + ", ".join(str(x) for x in self.coordinates) + ")"
    
    def distance(self, point):
        """
        """
        return linalg.norm(array(self.coordinates) - array(point.coordinates))
        
    def set_solution(self, solution):
        """
        """
        self.solution = solution
        # Remove the nill solution from the coordinates array.
        self.coordinates.pop(-1)
        # Append the real solution
        self.coordinates.append(solution)