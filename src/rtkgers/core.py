"""
The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2013 - Present Aaron Zampaglione
"""
from common.node import Node
from kgers.weights import KGERSWeights

class RTKGERSCore():
    
    def __init__(self, points):
        """
        """
        self.root = None
        self.points = points
        self.min_points = 3 * points[0].dimension
        
    def populate(self):
        """
        """
        
        self.root = Node()
        self.root.feature = None
        self.root.threshold = None
        self.root.hyperplane = KGERSWeights(self.points)
        self.root.hyperplane.execute()
        
        self.grow(self.root, self.points)
    
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
            points = sorted(points, key=lambda x: x.features[f])
            for i in range(self.min_points, len(points) - self.min_points):
                left_points = points[:i]
                right_points = points[i:]
            
                left = KGERSWeights(left_points)
                right = KGERSWeights(right_points)
            
                left.execute()
                right.execute()
            
                error = (len(left_points) / float(len(points))) * left.error() + \
                        (len(right_points) / float(len(points))) * right.error()
            
                if (best_error > error):
                    best_index = i
                    best_feature = f
                    best_error = error
                    best_left = left
                    best_right = right
        
        if (best_index != None):
            node.feature = best_feature
            node.threshold = points[best_index].features[best_feature]
            
            node.left = Node()
            node.left.feature = node.feature
            node.left.hyperplane = best_left
            
            self.grow(node.left, points[:best_index])
            
            node.right = Node()
            node.right.feature = node.feature
            node.right.hyperplane = best_right
            
            self.grow(node.right, points[best_index:])