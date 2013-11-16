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

class KGERSCore(object):
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, points):
        """
        """
        # We need a minimum of 3(n + 1) points for test, training, and validation.
        if (len(points) < 3 * (points[0].dimension + 1)):
            raise Exception("Not enough points to train, validate, and sample on.")
        
        # Initialize coefficients variable.
        self.coefficients = []
        
        # Get the test and training sets.
        self.test = self.sample(points, check=False)
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
        return sum([pow(self.solve(point) - point.solution, 2) for point in self.test])
        
    def sample(self, points, size = None, exclude = [], check = True):
        """
        """
        # If no size was specified, use the dimension of the points.
        if (size == None):
            size = points[0].dimension
        
        # Take a random sampling, but do not include the excluded group.
        samples = random.sample(set(points).difference(set(exclude)), size)
        
        # Make sure all the features are not the same for all the samples.
        if (check):
            for i in range(0, len(samples)):
                for j in range(i, len(samples)):
                    # As long as two samples have different features, everything will be solvable.
                    if set(samples[i].features) != set(samples[j].features):
                        return samples
        else:
            return samples
        
        # Re-sample and make sure not to include the first item.
        return self.sample(size=size, exclude=[samples[0]])

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