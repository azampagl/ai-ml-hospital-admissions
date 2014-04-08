"""
The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.4
@copyright 2014 - Present Aaron Zampaglione
"""
import csv
import getopt
import math
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
    
    # Skip the first line.
    reader.next()
    # Get a list of all the points.
    for row in reader:            
        points.append(Point([float(feature) for feature in row[2:]], float(row[1])))
    
    # Run the test against each of the algorithms.
    for algorithm in ['KGERSOriginal', 'KGERSWeights', 'KGERSDiameterWeights', 'KGERSDiameter']:
        print(algorithm)
        
        total = 10000
        avg = 0
        
        raw_errors = []
        display_errors = {}
        
        # Run KGERS x times and round the RMSE to the nearest .1
        for i in range(total):
          kgers = globals()[algorithm](points)
          kgers.execute(k=5)
          
          error = kgers.error()
          
          raw_errors.append(error)
          
          display_error = str(round(error, 1))
          
          if display_error in display_errors:
              display_errors[display_error] += 1
          else:
              display_errors[display_error] = 1
        
        # Display all the error ranges.
        for k in [str(x * 0.1) for x in range(0, 201)]:
          if k in display_errors:
            print(str(k) + "\t" + str(display_errors[k]))
          else:    
            print(str(k) + "\t" + str("0"))
        
        # Determine the standard deviation.
        avg = sum(raw_errors) / float(total)
        stdev = math.sqrt(sum([math.pow(e - avg, 2) for e in raw_errors]) / float(total))
        print(stdev)
        
        print("\n")

def usage():
    """Prints the usage of the program."""
    
    print("\n" + 
          "The following are arguments required:\n" + 
          "-i " +
          "\n" + 
          "Example Usage:\n" + 
          "python kgers-rmse-freq.py -i sampledata.csv\n" +
          "\n")

"""Main execution."""
if __name__ == "__main__":
    main()