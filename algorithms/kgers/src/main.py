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

import matplotlib.pyplot as plot

from timeit import default_timer

from hyperplane import Hyperplane
from kgers.original import KGERSOriginal
from kgers.diameter import KGERSDiameter
from kgers.weights import KGERSWeights
from point import Point

kgers = None

def main():
    """Main execution for the feature extractor."""
    
    # Determine command line arguments.
    try:
        rawopts, _ = getopt.getopt(sys.argv[1:], 'i:t:p:')
    except getopt.GetoptError:
        usage()
        sys.exit(2)
        
    opts = {}
    
    # Process each command line argument.
    for o, a in rawopts:
        opts[o[1]] = a
    
    # The following arguments are required in all cases.
    for opt in ['i', 't', 'p']:
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
    
    # Find the max coordinates
    max_x = max([point.coordinates[0] for point in points])
    max_y = max([point.coordinates[1] for point in points])
    min_x = min([point.coordinates[0] for point in points])
    min_y = min([point.coordinates[1] for point in points])
    
    # Draw all the points, if necessary.
    if opts['p']:
        plot.plot(
            [point.coordinates[0] for point in points],
            [point.coordinates[1] for point in points],
            'ro'
        )
    
    # Initialize our results struct(s).
    results = {}
    for algorithms in [('KGERSOriginal', 'b-'), ('KGERSDiameter', 'r-'), ('KGERSWeights', 'g-')]:
        algorithm, color = algorithms
        results[algorithm] = {}
        results[algorithm]['time'] = 0.0
        results[algorithm]['error'] = 0.0
        
        # Run each algorithm the number of times specified.
        for i in range(0, int(opts['t'])):
            kgers = globals()[algorithm](points)
            start = default_timer()
            kgers.execute()
            results[algorithm]['time'] = default_timer() - start
            results[algorithm]['error'] += kgers.error();
            
            # Plot the results.
            if (opts['p']):
                start_point = Point([min(min_x, 0.0)])
                end_point = Point([max(max_x, 10.0)])
                
                start_point.set_solution(kgers.solve(start_point))
                end_point.set_solution(kgers.solve(end_point))
                
                plot.plot(
                    [start_point.coordinates[0], end_point.coordinates[0]],
                    [start_point.coordinates[1], end_point.coordinates[1]],
                    color
                )
    
    # Print the results.
    for key in results.keys():
        print(key)
        print('\tError:\t' + str(results[key]['error'] / float(opts['t'])))
        print('\tTime:\t' + str(results[key]['time'] / float(opts['t'])))
    
    # Actually draw the graph, if requested.
    if opts['p']:
        plot.axis([min(min_x, 0.0), max(max_x, 10.0), min(min_y, 0.0), max(max_y, 10.0)])
        plot.show()

def usage():
    """Prints the usage of the program."""
    
    print("\n" + 
          "The following are arguments required:\n" + 
          "-i: the input file containing the feature data.\n" +
          "-t: the number of trials to execute.\n" +
          "-p: wheter or not to plot the data.\n" +
          "\n" + 
          "Example Usage:\n" + 
          "python main.py -i \"features.csv\" -t \"20\" -p \"1\"" +
          "\n")

"""Main execution."""
if __name__ == "__main__":
    main()