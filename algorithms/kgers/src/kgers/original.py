"""
The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2013 - Present Aaron Zampaglione
"""
from core import KGERSCore
from .hyperplane import Hyperplane

class KGERSOriginal(KGERSCore):
    
    def execute(self, k = 2):
        """
        """
        self.hyperplanes = []
        self.weights = []
        
        for i in range(0, k):
            # Grab a set of samples from the data set.
            samples = self.samples()
            # Grab a set of validators that are not in the sample set, and skip validation checks.
            validators = self.samples(exclude=samples, check=False)
            
            #print("Samples:" + str([str(point) for point in samples]))
            #print("Validators:" + str([str(point) for point in validators]))
            
            # Generate a hyperplane.
            hyperplane = Hyperplane(samples)
            self.hyperplanes.append(hyperplane)
            
            # Find the weight.
            self.weights.append(self.weigh(hyperplane, validators))
        
        self.average()