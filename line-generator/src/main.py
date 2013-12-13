"""
Generates a line with a normal distribution of noise.

The output is in the same format as the input acceptd by KGERS.

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
import numpy

def main():
    """Main execution for the feature extractor."""
    
    # Determine command line arguments.
    try:
        rawopts, _ = getopt.getopt(sys.argv[1:], 'n:h:l:s:y:v:o:')
    except getopt.GetoptError:
        usage()
        sys.exit(2)
        
    opts = {}
    
    # Process each command line argument.
    for o, a in rawopts:
        opts[o[1]] = a
    
    # The following arguments are required in all cases.
    for opt in ['n', 'h', 'l', 's', 'y', 'v', 'o']:
        if not opt in opts:
            usage()
            sys.exit(2)
    
    # Determine a random distribution to add to the y values of the perfect line.
    variance = float(opts['v'])
    distribution = [0.0] * int(opts['n'])
    if (variance != 0.0):
        distribution = [x * int(opts['n']) for x in numpy.random.normal(0, float(opts['v']), int(opts['n']))]
    
    # Determine a random number of "x" (feature) values.
    features = random.sample(xrange(int(opts['l']), int(opts['h'])), int(opts['n']))
    
    # Determine the "y" values of the graph.
    values = [f * float(opts['s']) + d + float(opts['y']) for f, d in zip(features, distribution)]
    
    # Determine the average of the y values.
    average = numpy.mean(values)
    
    # Write our results to the desired output file.
    writer = csv.writer(open(opts['o'], 'wb'), delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    
    # Write the header row.
    writer.writerow(['Period', 'Admissions', 'Feature1'])
    
    # Write each point to the csv file.
    for f, v in zip(features, values):
        writer.writerow([average, v, f])
    
def usage():
    """Prints the usage of the program."""
    
    print("\n" + 
          "The following are arguments required:\n" + 
          "-n: the number of points to generate.\n" +
          "-h: the maximum X value to generate.\n" +
          "-l: the lowest X value to generate.\n" +
          "-s: the slope of the line.\n" +
          "-y: the y-offset for the line.\n" +
          "-v: the variance of the normal distribution.\n" +
          "-o: the location of the output file.\n" +
          "\n" + 
          "Example Usage:\n" + 
          "python main.py -n 10 -h 10 -l 0 -s 3 -v 0.5 -o kgers-sample04.csv\n" +
          "\n")

"""Main execution."""
if __name__ == "__main__":
    main()