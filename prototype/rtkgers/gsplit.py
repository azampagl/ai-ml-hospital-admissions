"""
The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2013 - Present Aaron Zampaglione
"""
from common.node import Node

from common.hyperplane_exception import HyperplaneException
from kgers.original import KGERSOriginal
from kgers.diameter import KGERSDiameter
from kgers.weights import KGERSWeights
from kgers.diameterweights import KGERSDiameterWeights

from rtkgers.core import RTKGERSCore

class RTKGERSGreedySplit(RTKGERSCore):
    """
    """
    
    def grow(self, node, points):
        """
        """
        node.points = points
        
        # Return if we do not have enough points to split.
        if (len(points) < self.min_points * 2):
            return
        
        best_index = None
        best_feature = None
        best_left = None
        best_right = None
        best_error = node.hyperplane.error()
        
        for f in range(len(points[0].features)):
            points = sorted(node.points, key=lambda x: x.features[f])
            
            while (len(points) > self.min_points * 2):
                i = int(len(points) / 2)
                
                print("Splitting -\t" + self.algorithm + "\t- Feature -\t" + str(f) + "\t- Index -\t" + str(i))
            
                left_points = points[:i]
                right_points = points[i:]
            
                left = globals()[self.algorithm](left_points)
                right = globals()[self.algorithm](right_points)
            
                # Try to generate a hyperplane.
                try:
                    left.execute()
                    right.execute()
                except HyperplaneException, e:
                    break
                
                left_error = left.error()
                right_error = right.error()
                
                error = (len(left_points) / float(len(points))) * left_error + \
                        (len(right_points) / float(len(points))) * right_error
                
                if (best_error > error):
                    best_index = i
                    best_feature = f
                    best_error = error
                    best_left = left
                    best_right = right
                  
                if (right_error > left_error):
                    points = right_points
                else:
                    points = left_points
        
        if (best_index != None):
            node.feature = best_feature
            node.threshold = node.points[best_index].features[best_feature]
            
            node.left = Node()
            node.left.hyperplane = best_left
            
            self.grow(node.left, node.points[:best_index])
            
            node.right = Node()
            node.right.hyperplane = best_right
            
            self.grow(node.right, node.points[best_index:])