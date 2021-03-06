"""
The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2013 - Present Aaron Zampaglione
"""
from core import KGERSCore
from common.hyperplane import Hyperplane
from common.hyperplane_exception import HyperplaneException

class KGERSOriginal(KGERSCore):

    def execute(self, k = 10):
        """
        """
        self.hyperplanes = []
        self.weights = []
        for i in range(0, k):
            # Grab a set of samples from the data set.
            samples = self.sample(self.training)
            
            # Keep trying to generate a hyperplane 
            #  until one is successfully created.
            count = 0
            hyperplane = None
            while (count < self.MAX_HYPERPLANE_ATTEMPTS):
                try:
                    # Generate a hyperplane.
                    hyperplane = Hyperplane(samples)
                    break
                except HyperplaneException, e:
                    count += 1
                    samples = self.sample(self.training)
            
            if (count >= self.MAX_HYPERPLANE_ATTEMPTS):
                raise HyperplaneException("Failed to generate a hyperplane.")
            
            # Grab a set of validators that are not in the sample set, and skip validation checks.
            validators = self.sample(self.training, exclude=samples)
            
            self.hyperplanes.append(hyperplane)
            
            # Find the weight.
            self.weights.append(self.weigh(hyperplane, validators))
            #print(hyperplanes[-1].coefficients)
            #print(weights[-1])
        
        self.coefficients = self.average(self.hyperplanes, self.weights)