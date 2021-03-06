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

import numpy

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
    
    #
    # Start analysis.
    #
    
    ACTUALS = [3, 2, 1]
    
    K = 10
    
    # Keep track of stats for each coefficient.
    stats = []
    for i in range(0, len(ACTUALS)):
        stats.append([])
        for j in range(0, K + 1):
            stats[-1].append([])
    
    # Dump the error and hyperplanes to a file for each coefficient (+ constant)
    handles = []
    for i in range(0, len(ACTUALS)):
        handles.append(open("output" + str(i), "a+b"))
    
    # Run a large amount of trials and find out how many hyperplanes are above the actual values.
    for i in range(10000):
        above = [0] * len(ACTUALS)
        
        kgers = KGERSOriginal(points)
        kgers.execute(k=K)
        
        for hyperplane in kgers.hyperplanes:
            for j in range(len(hyperplane.coefficients)):
                if (hyperplane.coefficients[j] > ACTUALS[j] * 1.00):
                    above[j] += 1
        
        for j in range(len(hyperplane.coefficients)):
            stats[j][above[j]].append(kgers.error())
            handles[j].write(str(above[j]) + "\t" + str(kgers.error()) + "\n")
    
    # Calculate stats for each coefficient.
    for i in range(0, len(ACTUALS)):
        print ("Coefficient " + str(i))
        print("\tAbove\tTotal\tMean\tStdev")
        for j in range(0, K + 1):
            print("\t" + str(j) + "\t" + str(len(stats[i][j])) + "\t" + str(round(numpy.mean(stats[i][j]), 3)) + "\t" + str(round(numpy.std(stats[i][j]), 3)))
        print("\n")

def usage():
    """Prints the usage of the program."""
    
    print("\n" + 
          "\n" + 
          "\n")

"""Main execution."""
if __name__ == "__main__":
    main()