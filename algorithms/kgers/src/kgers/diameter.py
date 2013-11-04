"""
The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2013 - Present Aaron Zampaglione
"""
from Queue import PriorityQueue

from core import KGERSCore
from .hyperplane import Hyperplane

class KGERSDiameter(KGERSCore):
    
    def execute(self, k = 10, l = 2):
        """
        """
        self.hyperplanes = []
        self.weights = []
        
        for i in range(0, k):
            # Take multiple sample subsets and find the "largest" by dimension.
            samples_queue = PriorityQueue()
            for j in range(0, l):
                samples = self.samples()
                samples_size = len(samples)
                diameter = 0.0
                # Find the diameter based on the distance between each segment.
                for sample_index in range(0, samples_size):
                     diameter += samples[sample_index].distance(samples[(sample_index + 1) % samples_size])
                # Add the sample se
                samples_queue.put((1.0 / diameter, samples))
            
            # The sample set desired is is the first in the queue.
            samples = samples_queue.get()[1]
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