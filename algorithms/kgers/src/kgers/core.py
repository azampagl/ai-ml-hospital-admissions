"""
The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2013 - Present Aaron Zampaglione
"""
import abc

from math import pow
from random import sample

class KGERSCore(object):
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, points):
        """
        """
        self.points = points
    
    @abc.abstractmethod
    def execute(self, k = 3):
        """
        """
        return
    
    def average(self):
        """
        """
        # Find the total weight
        total_weight = sum(self.weights)
        
        # Find the length of the hyperplane coefficients.
        hyperplane_len = len(self.hyperplanes[0].coefficients)
        # Initialize coefficients to 0.
        self.coefficients = [0] * hyperplane_len
        
        for i in range(0, len(self.hyperplanes)):
            hyperplane = self.hyperplanes[i]
            hyperplane_weight = self.weights[i] / total_weight
            for j in range(0, hyperplane_len):
                self.coefficients[j] += hyperplane.coefficients[j] * hyperplane_weight
    
    def error(self):
        """
        """
        return sum([pow(self.solve(point) - point.solution, 2) for point in self.points])
        
    def samples(self, size = None, exclude = [], check = True):
        """
        """
        # If no size was specified, use the dimension of the points.
        if (size == None):
            size = self.points[0].dimension
        
        # Take a random sampling, but do not include the excluded group.
        samples = sample(set(self.points).difference(set(exclude)), size)
        
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
        return self.samples(exclude=[samples[0]])

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