"""
The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2013 - Present Aaron Zampaglione
"""
import abc
import math

from common.node import Node
from common.hyperplane_exception import HyperplaneException

from kgers.original import KGERSOriginal
from kgers.diameter import KGERSDiameter
from kgers.weights import KGERSWeights
from kgers.diameterweights import KGERSDiameterWeights

class RTKGERSCore():
    """
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, algorithm, points):
        """
        """
        self.root = None
        self.points = points
        self.algorithm = algorithm
        self.min_points = 3 * points[0].dimension
    
    def error(self, test):
        """
        """
        return math.sqrt(sum([pow(self.solve(point) - point.solution, 2) for point in test]) / float(len(test)))
    
    @abc.abstractmethod
    def grow(self, node, points):
        """
        """
        return
        
    def populate(self):
        """
        """
        
        self.root = Node()
        self.root.feature = None
        self.root.threshold = None
        self.root.hyperplane = globals()[self.algorithm](self.points)
        self.root.hyperplane.execute()
        
        self.grow(self.root, self.points)
        
    def solve(self, point):
        """
        """
        
        node = self.root
        while (node.left != None and node.right != None):
            if (point.features[node.feature] < node.threshold):
                node = node.left
            else:
                node = node.right
        
        #print(node)
        return node.hyperplane.solve(point)