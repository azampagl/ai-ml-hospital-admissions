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

def main():
    """Main execution method."""
    # Determine command line arguments.
    try:
        rawopts, _ = getopt.getopt(sys.argv[1:], 'i:o:')
    except getopt.GetoptError:
        usage()
        sys.exit(2)
        
    opts = {}
    
    # Process each command line argument.
    for o, a in rawopts:
        opts[o[1]] = a
    
    # The following arguments are required in all cases.
    for opt in ['i', 'o']:
        if not opt in opts:
            usage()
            sys.exit(2)
    
    # Create our reader and output files.
    reader = csv.reader(open(opts['i'], 'rb'), delimiter=',', quotechar='|') 
    out = open(opts['o'], 'w')
     
    # Skip the first line
    reader.next()
    for row in reader:            
        out.write("{0} 1:{1} 2:{2} 3:{3} 4:{4} 5:{5} 6:{6}\n".format(*row[1:]))
    
def usage():
    """Prints the usage of the program."""
    print("\n" + 
          "The following are arguments required:\n" + 
          "-i: the feature file.\n" +
          "-o: the output file.\n" +
          "\n" + 
          "Example Usage:\n" + 
          "python main.py -i \"../data\" -o \"feature.csv\"" +
          "\n")

"""Main execution."""
if __name__ == "__main__":
    main()