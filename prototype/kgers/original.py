"""
The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2013 - Present Aaron Zampaglione
"""
from core import KGERSCore
from common.hyperplane import Hyperplane

class KGERSOriginal(KGERSCore):

    def execute(self, k = 10):
        """
        """
        hyperplanes = []
        weights = []
        for i in range(0, k):
            # Grab a set of samples from the data set.
            samples = self.sample(self.training)
            # Grab a set of validators that are not in the sample set, and skip validation checks.
            validators = self.sample(self.training, exclude=samples, check=False)
            
            # Generate a hyperplane.
            hyperplane = Hyperplane(samples)
            hyperplanes.append(hyperplane)
            
            # Find the weight.
            weights.append(self.weigh(hyperplane, validators))
        
        self.coefficients = self.average(hyperplanes, weights)