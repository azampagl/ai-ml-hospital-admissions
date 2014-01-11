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

from common.hyperplane import Hyperplane
from common.point import Point
from kgers.original import KGERSOriginal
from kgers.diameter import KGERSDiameter
from kgers.weights import KGERSWeights
from kgers.diameterweights import KGERSDiameterWeights

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
    points = []
    
    # Skip the first line
    reader.next()
    for row in reader:            
        points.append(Point([float(feature) for feature in row[2:]], float(row[1])))
    
    point1 = points[2]
    point2 = points[8]
    point3 = points[6]
    
    #tmp = 0.0
    
    #tmp = point1.features[0]
    #point1.features[0] = point1.features[1]
    #point1.features[1] = tmp
    
    #tmp = point2.features[0]
    #point2.features[0] = point2.features[1]
    #point2.features[1] = tmp
    
    #tmp = point3.features[0]
    #point3.features[0] = point3.features[1]
    #point3.features[1] = tmp
    
    #h = Hyperplane([point1, point2, point3])
    #h.execute()
    #print(h.coefficients)
    
    #print(
    #    np.allclose(
    #        np.dot([point1.solution, point2.coefficients, point3.coefficients], h.coefficients), [point1.solution, point2.solution, point3.solution])
    #    )
    
    for algorithm in ['KGERSOriginal']:#, 'KGERSWeights', 'KGERSDiameterWeights', 'KGERSDiameter']:
        kgers = globals()[algorithm](points)
        kgers.execute(k=3)
        print("Final:\t" + str(kgers.coefficients))
        print("Error:\t" + str(kgers.error()))

def usage():
    """Prints the usage of the program."""
    
    print("\n" + 
          "The following are arguments required:\n" + 
          "-i " +
          "\n" + 
          "Example Usage:\n" + 
          "python main.py -c 2,3,1 -n 10 -h 10,10 -l -10,-10 -s .01 -o kgers-sample04.csv\n" +
          "\n")

"""Main execution."""
if __name__ == "__main__":
    main()