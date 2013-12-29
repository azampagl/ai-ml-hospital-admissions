"""
See class definition.

The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2013 - Present Aaron Zampaglione
"""
from scipy import array
from scipy.linalg import lu

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
        # Build our linear equation matrix
        matrix = []
        for point in points:
            # Grab a copy of the coordinates.
            row = list(point.coordinates)
            # Insert the constant as the last column of the feature part of the matrix.
            row.insert(-1, 1.0)
            matrix.append(row)
        
        # Perform gaussian elimination using lu decomposition.
        pl, u = lu(array(matrix), permute_l=True)
        
        # Matrix attributes.
        rows = len(u)
        cols = rows
        
        # Current row to be evaluated.
        current_row = rows - 1
        
        # Find the last row that isn't all zeros.
        while (sum(u[current_row][:-1]) == 0.0):
            current_row -= 1
        
        # Set the coefficients
        self.coefficients = [u[current_row][-1] / u[current_row][-2]]
        
        # Backsolve, starting with the second to last solved row.
        for i in reversed(range(0, current_row)):
            row_sum = 0.0
            # Start with the second to last column.
            for j in reversed(range(i + 1, cols - 1)):
                row_sum += u[i][j] * self.coefficients[j - i - 1]
            self.coefficients.insert(0, (u[i][cols - 1] - row_sum) / u[i][i])
        
    def solve(self, point):
        """
        Given a set a features, returns the predicted solution.
        """
        # Solve the linear equation with the features given.
        return sum([a * b for a, b in zip(self.coefficients[:-1], point.features)]) \
            + self.coefficients[-1]