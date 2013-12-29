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
    
    h = Hyperplane(points[0:4])
    #for algorithm in ['KGERSOriginal']:
    #    kgers = globals()[algorithm](points)
    #    kgers.execute(k=1)
    #    print(kgers.coefficients)

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