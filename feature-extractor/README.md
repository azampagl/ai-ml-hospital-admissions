# feature-extractor #

This is directory contains the feature extractor application. It is a suite of python scripts that read in the raw data set provided by the hospital and outputs a csv file containing the desired features.

## File Structure ##

* **src**

  The source code.

## Usage ##

The extractor can be executed by running **main.py** in the **src/** directory. Executing the script with no parameters will print the detailed usage.

``python main.py``

Some example usages are:

``python main.py -i ../../data/EDinpt12.csv -o ../../tmp/train.features.csv -s "2008/04/01" -e "2010/03/01"``


``python main.py -i ../../data/EDinpt12.csv -o ../../tmp/test.features.csv -s "2010/04/01" -e "2011/03/01"``