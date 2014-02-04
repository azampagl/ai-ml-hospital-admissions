"""
This script is used to see how resillient KGERS is to noisy data.

This script generates multiple noisey linear lines, with increasing deviation
in noise, and evaluates how the various implementions of KGERS react.

The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.4
@copyright 2013 - Present Aaron Zampaglione
"""
import csv
import getopt
import os
import shutil
import sys

from timeit import default_timer

from common.point import Point

from kgers.original import KGERSOriginal
from kgers.diameter import KGERSDiameter
from kgers.weights import KGERSWeights
from kgers.diameterweights import KGERSDiameterWeights

def main():
    """Main execution for the feature extractor."""
    
    # Determine command line arguments.
    try:
        rawopts, _ = getopt.getopt(sys.argv[1:], 'o:t:')
    except getopt.GetoptError:
        usage()
        sys.exit(2)
        
    opts = {}
    
    # Process each command line argument.
    for o, a in rawopts:
        opts[o[1]] = a
    
    # The following arguments are required in all cases.
    for opt in ['o', 't']:
        if not opt in opts:
            usage()
            sys.exit(2)
    
    # Remove and create the storage directory.
    if os.path.exists(opts['o']):
        shutil.rmtree(opts['o'])
    os.mkdir(opts['o']) 
    
    # Init results dictionary. Each algorithm will have a linked list of
    #  error results from each data set.
    results = {}
    for algorithm in ['KGERSOriginal', 'KGERSDiameter', 'KGERSWeights', 'KGERSDiameterWeights']:
        results[algorithm] = []
    
    for i in range(0, 11):
        file = opts['o'] + "/kgers-sample0" + str(i) + ".csv"
        os.system(
            "python ../data-generator/src/main.py \
            -c 3,2,1 \
            -n 20 \
            -h 101,101 \
            -l 1,1 \
            -s " + str(0.01 * i) + " \
            -o " + file)
        
        # Create our reader and output files.
        reader = csv.reader(open(file, 'rb'), delimiter=',', quotechar='|') 
    
        # The points are essentially feature sets with the known solution.
        points = []
    
        # Skip the first line
        reader.next()
        for row in reader:            
            points.append(Point([float(feature) for feature in row[2:]], float(row[1])))
        
        # Initialize our results struct(s).
        for algorithm in ['KGERSOriginal', 'KGERSDiameter', 'KGERSWeights', 'KGERSDiameterWeights']:
            # Keep track of the time to run and error for each result.
            time = 0.0
            error = 0.0
            
            for t in range(int(opts['t'])):
                kgers = globals()[algorithm](points)
                start = default_timer()
                kgers.execute()
                time += default_timer() - start
                error += kgers.error();
            
            results[algorithm].append(error / int(opts['t']))
        
    for algorithm in results.keys():
        print(algorithm)
        for i in range(len(results[algorithm])):
            print("\t" + str(0.01 * i) + "\t" + str(results[algorithm][i]))
        print("")

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