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

class RTKGERSDepthGreedySplit(RTKGERSCore):
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
            
            i = 0
            
            last_left = None
            last_right = None
            last_error = None
            
            indicies = []
            while (len(points) > self.min_points * 2):
                half = int(len(points) / 2)
                i += half
                
                indicies.append(i)
                
                #print("Splitting -\t" + self.algorithm + "\t- Feature -\t" + str(f) + "\t- Index -\t" + str(i))
                #print("Feature -\t" + str(f) + "\t- Index -\t" + str(i) + "\t- Len -\t" + str(len(points)))
                print("Index\t\t" + str(i + node.index))
                
                left_points = points[:half]
                right_points = points[half:]
                print("Left Size\t"  + str(len(left_points)))
                print("Right Size\t" + str(len(right_points)))
                
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
                
                print("LeftError\t" + str(left_error))
                print("RightError\t" + str(right_error))
                print("")
                
                if (right_error > left_error):
                    print("Right")
                    points = right_points
                else:
                    print("Left")
                    i -= half
                    points = left_points
            
            #
            #
            #
            
            points = sorted(node.points, key=lambda x: x.features[f])
            while len(indicies) > 0:
                i = indicies.pop()
                
                left_points = points[:i]
                right_points = points[i:]

                print("Left Size\t"  + str(len(left_points)))
                print("Right Size\t" + str(len(right_points)))
                
                left = globals()[self.algorithm](left_points)
                right = globals()[self.algorithm](right_points)
            
                # Try to generate a hyperplane.
                try:
                    left.execute()
                    right.execute()
                except HyperplaneException, e:
                    continue
                
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
            
        if (best_index != None):
            print("Splitting at " + str(best_index + node.index))
            print("")
            node.feature = best_feature
            node.threshold = node.points[best_index].features[best_feature]
            
            
            node.left = Node()
            node.left.hyperplane = best_left
            node.left.index = best_index
            
            #print("Growing Left - " + str(len(node.points[:best_index])))
            #print("")
            self.grow(node.left, node.points[:best_index])
            
            node.right = Node()
            node.right.hyperplane = best_right
            node.right.index = best_index
            
            #print("Growing Right - " + str(len(node.points[best_index:])))
            #print("")
            self.grow(node.right, node.points[best_index:])
            
        else:
            print("")
            #print("Best error was not defeated - " + str(len(points)))