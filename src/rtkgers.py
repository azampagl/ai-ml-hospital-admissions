"""
The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2013 - Present Aaron Zampaglione
"""
from node import Node
from ..kgers.kgers.diameterweights import KGERSDiameterWeights

class RTKGERS():
    
    def __init__(self, points):
        """
        """
        self.root = Node()
        self.points = points
    
    def execute(self):
        """
        """
        self.root.hyperplane = KGERSDiameterWeights(points)
        self.root.hyperplane.execute()
        print(self.root.hyperplane.coefficients)