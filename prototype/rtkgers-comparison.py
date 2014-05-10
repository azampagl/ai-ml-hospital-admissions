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
import random
import sys
import math
import time

import matplotlib.pyplot as plot

from rtkgers.original import RTKGERSOriginal
from rtkgers.gsplit import RTKGERSGreedySplit
from rtkgers.depthgsplit import RTKGERSDepthGreedySplit

from common.point import Point

def main():
    """Main execution for the feature extractor."""
    
    # Determine command line arguments.
    try:
        rawopts, _ = getopt.getopt(sys.argv[1:], 't:v:o:')
    except getopt.GetoptError:
        usage()
        sys.exit(2)
        
    opts = {}
    
    # Process each command line argument.
    for o, a in rawopts:
        opts[o[1]] = a
    
    # The following arguments are required in all cases.
    for opt in ['t', 'v', 'o']:
        if not opt in opts:
            usage()
            sys.exit(2)
    
    training_reader = csv.reader(open(opts['t'], 'rb'), delimiter=',', quotechar='|') 
    training = []
    # Skip the first line
    training_reader.next()
    for row in training_reader:            
        training.append(Point([float(feature) for feature in row[2:]], float(row[1])))
    
    test_reader = csv.reader(open(opts['v'], 'rb'), delimiter=',', quotechar='|') 
    test = []
    # Skip the first line
    test_reader.next()
    for row in test_reader:            
        test.append(Point([float(feature) for feature in row[2:]], float(row[1])))
    
    # Output file
    out = open(opts['o'], 'w')
    
    # Run the test against each of the algorithms.
    for algorithm in ['RTKGERSDepthGreedySplit', 'RTKGERSOriginal']:
        out.write(algorithm + "\n")
        
        total = 30
        avg = 0
        
        times = []
        raw_errors = []
        display_errors = {}
        
        # Run KGERS x times and round the RMSE to the nearest .1
        for i in range(total):
          rtkgers = globals()[algorithm]('KGERSWeights', training)
          start = time.time()
          rtkgers.populate()
          times.append(time.time() - start)
          
          error = rtkgers.error(test)
          
          raw_errors.append(error)
          
          display_error = str(round(error, 1))
          
          if display_error in display_errors:
              display_errors[display_error] += 1
          else:
              display_errors[display_error] = 1
        
        # Display all the error ranges.
        for k in [str(x * 0.1) for x in range(0, 101)]:
          if k in display_errors:
            out.write(str(k) + "\t" + str(display_errors[k]) + "\n")
          else:    
            out.write(str(k) + "\t" + str("0") + "\n")
        
        # Write the average runtime.
        out.write(str(sum(times) / len(times)) + "\n")
        
        # Determine the standard deviation.
        avg = sum(raw_errors) / float(total)
        stdev = math.sqrt(sum([math.pow(e - avg, 2) for e in raw_errors]) / float(total))
        out.write(str(stdev) + "\n\n")
        
    out.close()
    
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