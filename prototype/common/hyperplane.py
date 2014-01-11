"""
See class definition.

The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2013 - Present Aaron Zampaglione
"""
from scipy import array
from scipy.linalg import det
from scipy.linalg import lu
from scipy.linalg import solve

class Hyperplane():
    """
    A hyperplane represents an approximate solution for
    a given set of training features. Once a hyperplane is determined,
    it can be used to predict solution based on the features provided.
    """
    
    def __init__(self, points):
        """
        Creates a hyperlane (coefficients of a linear
        equation) based on the points given.
        """
        # Make sure we have the minimum number of points necessary.
        if len(points) > 0 and len(points) < points[0].dimension:
            raise Exception("Not enough points to make a hyperplane.")
        
        # Make sure we are provided with a rull rank matrix.
        if round(det(array([point.coordinates for point in points])), 1) == 0.0:
            raise Exception("The points provided are linearly dependent.")
        
        # Keep a reference to the points used to build the hyperplane
        self.points = points
        
        # Build our linear equation matrix
        a = []
        b = []
        for point in points:
            # Insert the constant as the last column of the feature part of the matrix.
            a.append(list(point.features) + [1.0])
            # Add to the solution of the matrix.
            b.append(point.solution)
        #print(a)
        # Solve to find the coefficients.
        self.coefficients = list(solve(a, b))
        #print([str(point) for point in points])
        #print(self.coefficients)
        
    def solve(self, point):
        """
        Given a set a features, returns the predicted solution.
        """
        # Solve the linear equation with the features given.
        return sum([a * b for a, b in zip(self.coefficients[:-1], point.features)]) \
            + self.coefficients[-1]