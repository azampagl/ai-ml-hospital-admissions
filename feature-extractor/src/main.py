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

from datetime import datetime, timedelta

from extractor.admission import Admission
from extractor.extractor import Extractor

def main():
    """Main execution for the feature extractor."""
    
    # Determine command line arguments.
    try:
        rawopts, _ = getopt.getopt(sys.argv[1:], 'i:o:s:e:')
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
    
    # Determine start date.
    start_date = None
    if ('s' in opts):
        start_date = datetime.strptime(opts['s'], '%Y/%m/%d')
    
    # Determine end date.
    end_date = None
    if ('e' in opts):
        end_date = datetime.strptime(opts['e'], '%Y/%m/%d')
    
    # Create admissions dictionary.
    admissions = {}
    
    # Read the input file and file and populate the admission dictionary.
    reader = csv.reader(open(opts['i'], 'rb'), delimiter=',', quotechar='|')
    
    # Skip the first line
    try:
        reader.next()
    except Exception:
        None

    for row in reader:
        # Create an admission based on the raw data from the file.
        admission = Admission.createFromRaw(row)
        
        # If the admission time is less than the start date + the max look back, skip.
        if ((not start_date is None) and ((admission.time + timedelta(weeks=Extractor.MAX_WEEK_LOOK_BACK)) < start_date)):
            continue
        # If the admission time is greater than the end date, skip.
        if ((not end_date is None) and (admission.time > end_date)):
            continue

        # Determine the key which is used for a dictionary lookup.
        key = admission.key()
        # Count the number of admission for that time slot.
        if (admissions.has_key(key)):
            admissions[key] += 1
        else:
            admissions[key] = 1
    
    # Sort the keys
    keys = admissions.keys()
    keys.sort()
    
    # Write our results to the desired output file.
    writer = csv.writer(open(opts['o'], 'wb'), delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    
    # Write the header row.
    writer.writerow(['Period', 'Admissions', 'Feature1', 'Feature2', 'Feature3', 'Feature4', 'Feature5', 'Feature6'])
    # For each key, find the features.
    for key in keys:
        # Create the admission based on the key.
        admission = Admission.createFromKey(key)
        # If the admission time is less than the start date, skip.
        if ((not start_date is None) and (admission.time < start_date)):
            continue
        # If the admission time is greater than the end date, skip.
        if ((not end_date is None) and (admission.time > end_date)):
            continue
    
        features = Extractor.features(admissions, key)
        # Only write to file if we have features.
        if not features is None:
            # Insert the period and the actual admissions into the feature set before we write to the file.
            features.insert(0, admissions[key])
            features.insert(0, key)
            writer.writerow(features)

def usage():
    """Prints the usage of the program."""
    
    print("\n" + 
          "The following are arguments required:\n" + 
          "-i: the input file containing the training/test data.\n" +
          "-o: the output file.\n" +
          "-s [optional]: the start date in 'YYYY/MM/DD' format.\n" +
          "-e [optional]: the end date in 'YYYY/MM/DD' format.\n" +
          "\n" + 
          "Example Usage:\n" + 
          "python main.py -i \"data.csv\" -o \"features.csv\"" +
          "\n")

"""Main execution."""
if __name__ == "__main__":
    main()