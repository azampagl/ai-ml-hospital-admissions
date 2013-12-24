"""
Generates a multidimentional data set with an optional
normal distribution of noise.

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
        rawopts, _ = getopt.getopt(sys.argv[1:], 'c:n:h:l:s:o:')
    except getopt.GetoptError:
        usage()
        sys.exit(2)
        
    opts = {}
    
    # Process each command line argument.
    for o, a in rawopts:
        opts[o[1]] = a
    
    # The following arguments are required in all cases.
    for opt in ['c', 'n', 'h', 'l', 's', 'o']:
        if not opt in opts:
            usage()
            sys.exit(2)
    
    # Determine the coefficients for the linear equation (Ax + By + C = z)
    coefficients = [float(c) for c in opts['c'].split(',')]
    
    # The number of features is the coefficients minus 1 (the constant).
    num_features = len(coefficients) - 1
    
    # The number of values to generate for each feature.
    num_feature_values = int(opts['n'])
    
    # The max vaues to use for each feature.
    max_feature_values = [float(x) for x in opts['h'].split(',')]
    
    # The max vaues to use for each feature.
    min_feature_values = [float(x) for x in opts['l'].split(',')]
    
    # Find the standard deviation.
    stdev = float(opts['s'])
    
    # Determine the base feature values.
    features = []
    for (i in num_features):
        features.append(
            random.sample(
                xrange(min_feature_values[i], max_feature_values[i]),
                num_feature_values
            )
        )
    
    # Determine the solution for each equation.
    solutions = []
    for (i in num_feature_values):
        solution = 0.0
        # Multiply the feature value by the coefficient
        for (j in num_features):
            solution += features[j][i] * coefficients[j]
        # Add the constant for the equation.
        solution += coefficients[-1]
        solutions.append(solution)

    # Determine a random distribution for each feature.
    noise = [0.0] * num_feature_values
    if (stdev != 0.0):
        noise = numpy.random.normal(0, stdev, num_feature_values)
    
    # Determine the magnitude for the feature set.
    mag = max(solutions) - min(solutions)
    
    # Add the random distribution (noise) to the solutions.
    for (i in num_feature_values):
      solutions[i] += noise[i] * mag
      
    # Write our results to the desired output file.
    writer = csv.writer(open(opts['o'], 'wb'), delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    
    # Write the header row.
    writer.writerow(
        ['Period', 'Admissions'].extend(
            ["Feature" + str(x) for x in num_features]
        )
    )
    
    # Write the data to disk.
    for (i in num_feature_values):
        writer.writerow(
            [i, solution[i]].extend(
                [features[x][i] for x in num_features]
            )
        )
    
def usage():
    """Prints the usage of the program."""
    
    print("\n" + 
          "The following are arguments required:\n" + 
          "-c: the coefficients of the linear equation (Ax + By + C)." +
          " Input should be provided in comma seperated form (e.g. for 3d data set -c 2,3,1).\n" +
          "-n: the number of values to generate for each feature.\n" +
          "-h: the maximum values to use for each feature." +
          " Input should be provided in comma seperated form (e.g. for 3d data set -h 200,30).\n" +  
          "-l: the lowest feature value to generate." +
          " Input should be provided in comma seperated form (e.g. for 3d data set -l 32,8).\n" +  
          "-s: the standard deviation of the normal distribution.\n" +
          "-o: the location of the output file.\n" +
          "\n" + 
          "Example Usage:\n" + 
          "python main.py -n 10 -h 10 -l 0 -s 3 -v 0.5 -o kgers-sample04.csv\n" +
          "\n")

"""Main execution."""
if __name__ == "__main__":
    main()