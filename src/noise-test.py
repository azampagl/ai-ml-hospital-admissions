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

import matplotlib.pyplot as plot

from rtkgers.original import RTKGERSOriginal
from common.point import Point

def main():
    """Main execution for the feature extractor."""
    
    # Determine command line arguments.
    try:
        rawopts, _ = getopt.getopt(sys.argv[1:], 'o:')
    except getopt.GetoptError:
        usage()
        sys.exit(2)
        
    opts = {}
    
    # Process each command line argument.
    for o, a in rawopts:
        opts[o[1]] = a
    
    # The following arguments are required in all cases.
    for opt in ['o']:
        if not opt in opts:
            usage()
            sys.exit(2)
    
    # Remove and create the storage directory.
    if os.path.exists(opts['o']):
        shutil.rmtree(opts['o'])
    os.mkdir(opts['o']) 
    
    for i in range(1, 10):
        os.system(
            "python ../line-generator/src/main.py \
            -n 1000 \
            -h 1000 \
            -l 0 \
            -s 1 \
            -y 100 \
            -v " + str(0.1 * i)+ " \
            -o " + opts['o'] + "/kgers-sample0" + str(i) + ".csv")

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