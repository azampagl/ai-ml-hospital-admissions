"""
The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.4
@copyright 2013 - Present Aaron Zampaglione
"""
import csv
import getopt
import os
import sys

#import matplotlib.pyplot as plot
#from pylab import *
#from mpl_toolkits.mplot3d import Axes3D

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from rtkgers.original import RTKGERSOriginal
from common.point import Point

def main():
    """Main execution for the feature extractor."""
    
    # Determine command line arguments.
    try:
        rawopts, _ = getopt.getopt(sys.argv[1:], 'i:')
    except getopt.GetoptError:
        usage()
        sys.exit(2)
        
    opts = {}
    
    # Process each command line argument.
    for o, a in rawopts:
        opts[o[1]] = a
    
    # The following arguments are required in all cases.
    for opt in ['i']:
        if not opt in opts:
            usage()
            sys.exit(2)
    
    # Create our reader and output files.
    reader = csv.reader(open(opts['i'], 'rb'), delimiter=',', quotechar='|') 
    
    # The points are essentially feature sets with the known solution.
    point_sets = {}
    
    # Skip the first line
    #reader.next()
    #for row in reader:
    #    if not row[0] in point_sets:
    #        point_sets[row[0]] = []       
    #    point_sets[row[0]].append(Point([float(feature) for feature in row[2:]], float(row[1])))
    
    #rtkgers = RTKGERSOriginal('KGERSWeights', points)
    #rtkgers.populate()

    # create x,y
    
    plt3d = plt.figure().gca(projection='3d')
    
    xx, yy = np.meshgrid(range(3), range(3))
    print(xx)
    z = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    plt3d.scatter(xx, yy, z)
    #for key in point_sets:
    #    points = point_sets[key]
    #
    #    max_x = int(max([p.coordinates[0] for p in points]))
    #    max_y = int(max([p.coordinates[1] for p in points]))
    #    xx, yy = np.meshgrid(range(max_x), range(max_y))
    
    #    z = []
    #    for x in range(max_x):
    #        z.append([0] * max_y)
    
    #    for point in points:
    #        z[int(point.coordinates[0]) - 1][int(point.coordinates[1]) - 1] = point.coordinates[2]
        
    #    plt3d.scatter(xx, yy, z)
    #z = [
    #        [0, 0, 0],
    ##        [1, 0, 0],
    #        [0, 0, 0]
    #    ]

    #R = np.sqrt(xx**2 + xx**2)
    #Z = np.sin(R)
    #print(z)

    # plot the surface
        
    #plt3d.plot_surface(xx, yy, z)
    #plt3d.plot_surface(xx, yy, Z)
        
        
    plt.show()


def usage():
    """Prints the usage of the program."""
    
    print("\n" + 
          "The following are arguments required:\n" + 
          "-i: the input file containing the feature data.\n" +
          "\n" + 
          "Example Usage:\n" + 
          "python main.py -i \"features.csv\"" +
          "\n")

"""Main execution."""
if __name__ == "__main__":
    main()