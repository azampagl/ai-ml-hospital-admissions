"""
This script will load the test feature set, the results from the 
SVM machine run, and find the absolute differece, percent difference,
Average percent difference, and the RMSE.

The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.4
@copyright 2013 - Present Aaron Zampaglione
"""
import csv
import getopt
import math
import os
import sys

def main():
    """Main execution method."""
    # Determine command line arguments.
    try:
        rawopts, _ = getopt.getopt(sys.argv[1:], 'f:s:o:')
    except getopt.GetoptError:
        usage()
        sys.exit(2)
        
    opts = {}
    
    # Process each command line argument.
    for o, a in rawopts:
        opts[o[1]] = a
    
    # The following arguments are required in all cases.
    for opt in ['f', 's', 'o']:
        if not opt in opts:
            usage()
            sys.exit(2)

    # Open our files.
    feature_file = open(opts['f'], 'rb')
    svm_file = open(opts['s'], 'r')
    result_file = open(opts['o'], 'wb')
    
    # Create the necessary csv readers and writers.
    reader = csv.reader(feature_file, delimiter=',', quotechar='|')
    writer = csv.writer(result_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    
    # Read the first line and add our additional headers.
    header = [
        'Period',
        'Actual Admissions',
        'Predicted Admissions',
        'Absolute Difference',
        'Absolute Percent Difference'
    ]
    writer.writerow(header)
    
    # Skip the first row, which contains headers.
    reader.next()
    
    total = 0
    total_percent_difference = 0
    rmse = 0
    
    for feature_row in reader:
        svm_row = svm_file.readline()
        
        # Perform Calculations
        actual = int(feature_row[1])
        predicted = float(svm_row.strip('\n'))
        
        abs_difference = math.fabs(actual - predicted)
        abs_percent_difference = math.fabs(actual - predicted) / actual
        
        total_percent_difference += abs_percent_difference
        rmse += (predicted - actual) ** 2
        
        total += 1
        
        row = [
            feature_row[0],
            actual,
            predicted,
            abs_difference,
            abs_percent_difference
        ]
        writer.writerow(row)
    
    print(total_percent_difference / total)
    print(math.sqrt(rmse / total))
    
def usage():
    """Prints the usage of the program."""
    print("\n" + 
          "The following are arguments required:\n" + 
          "-f: the feature file.\n" +
          "-s: the svm outpit file from the test data set.\n" +
          "-o: the output file.\n" +
          "\n" + 
          "Example Usage:\n" + 
          "python main.py -f \"features.csv\" -s \"test.svm\" -o \"results.csv\"" +
          "\n")

"""Main execution."""
if __name__ == "__main__":
    main()