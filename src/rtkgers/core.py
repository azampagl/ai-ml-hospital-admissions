"""
The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2013 - Present Aaron Zampaglione
"""
from common.node import Node
from kgers.diameterweights import KGERSDiameterWeights

class RTKGERSCore():
    
    def __init__(self, points):
        """
        """
        self.root = None
        self.points = points
        self.min_points = 3 * points[0].dimension + 3
        
    def populate(self):
        """
        """
        points = sorted(self.points, key=lambda x: x.features[0])
        
        self.root = Node()
        self.root.feature = 0
        self.root.hyperplane = KGERSDiameterWeights(points)
        self.root.hyperplane.execute()
        
        self.grow(self.root, points)
    
    def grow(self, node, points):
        """
        """
        node.points = points
        
        # Return if we do not have enough points to split.
        if (len(points) < self.min_points * 2):
            print("Returning " + str(len(points)))
            return
        
        best_index = None
        best_error = node.hyperplane.error()
        best_left = None
        best_right = None
        for i in range(self.min_points, len(points) - self.min_points):
            left_points = points[:i]
            right_points = points[i:]
            
            left = KGERSDiameterWeights(left_points)
            right = KGERSDiameterWeights(right_points)
            
            left.execute()
            right.execute()
            
            error = (len(left_points) / float(len(points))) * left.error() + \
                    (len(right_points) / float(len(points))) * right.error()
            
            print (str(node) + " - " + str(best_error) + " > " + str(error))
            if (best_error > error):
                best_index = i
                best_error = error
                best_left = left
                best_right = right
        
        print (str(best_index) + " - " + str(best_error))
        if (best_index != None):
            node.index = best_index
            node.threshold = points[best_index].features[node.feature]
            
            node.left = Node()
            node.left.feature = node.feature
            node.left.hyperplane = best_left
            
            print("Splitting left")
            self.grow(node.left, points[:best_index])
            
            node.right = Node()
            node.right.feature = node.feature
            node.right.hyperplane = best_right
            
            print("Splitting right")
            self.grow(node.right, points[best_index:])