"""
The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2013 - Present Aaron Zampaglione
"""
import abc
import math
import random

from common.hyperplane import Hyperplane

class KGERSCore(object):
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, points):
        """
        """
        # We need a minimum of 3(n + 1) points for test, training, and validation.
        if (len(points) == 0 or len(points) < 3 * (points[0].dimension)):
            raise Exception("Not enough points to train, validate, and sample on.")
        
        # Initialize coefficients variable.
        self.coefficients = []
        
        # Get the test and training sets.
        self.test = self.sample(
            points,
             # Take 30% of the data set for testing, or the minimum required.
            size=max([int(len(points) * .3), points[0].dimension]),
            check=False
        )
        self.training = list(set(points).difference(set(self.test)))
    
    @abc.abstractmethod
    def execute(self, k = 10):
        """
        """
        return
    
    def average(self, hyperplanes, weights):
        """
        """
        # Find the total weight
        total_weight = sum(weights)
        
        # Find the length of the hyperplane coefficients.
        hyperplane_len = len(hyperplanes[0].coefficients)
        # Initialize coefficients to 0.
        coefficients = [0] * hyperplane_len
        
        for i in range(0, len(hyperplanes)):
            hyperplane = hyperplanes[i]
            hyperplane_weight = weights[i] / total_weight
            
            for j in range(0, hyperplane_len):
                coefficients[j] += hyperplane.coefficients[j] * hyperplane_weight
        
        return coefficients
    
    def error(self):
        """
        """
        return sum([pow(self.solve(point) - point.solution, 2) for point in self.test]) / float(len(self.test))
        
    def sample(self, points, size = None, exclude = [], check = True):
        """
        """
        # If no size was specified, use the dimension of the points.
        if (size == None):
            size = points[0].dimension
        
        # Take a random sampling, but do not include the excluded group.
        return random.sample(set(points).difference(set(exclude)), size)

    def solve(self, point):
        """
        """
        # Solve the linear equation with the features given.
        return sum([a * b for a, b in zip(self.coefficients[:-1], point.features)]) \
            + self.coefficients[-1]

    def weigh(self, hyperplane, validators):
        """
        """
        summation = sum([pow(hyperplane.solve(validator) - validator.solution, 2) for validator in validators])
        
        if summation == 0.0:
            return 1.0
        
        return 1.0 / summation