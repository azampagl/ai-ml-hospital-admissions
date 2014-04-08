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
from scipy import array
from scipy.linalg import det
from scipy.linalg import lu
from scipy.linalg import solve
from scipy.linalg import lstsq

def main():
    """
    """
    
    a = [
        [1.0, 5.2, 1.0, 4.333333333333333, 3.0, 1.0, 1.0],
        [1.0, 5.4, 3.0, 7.0, -4.0, -1.0, 1.0],
        [1.0, 5.4, 2.0, 9.666666666666666, 2.0, -1.0, 1.0],
        [1.0, 2.0, 1.0, 5.0, -1.0, 3.0, 1.0],
        [1.0, 5.8, 5.0, 7.333333333333333, 3.0, -2.0, 1.0],
        [1.0, 2.8, 3.0, 6.666666666666667, 2.0, 4.0, 1.0],
        [1.0, 4.4, 4.0, 3.6666666666666665, -3.0, -3.0, 1.0],
    ]
    b = [6.0, 10.0, 3.0, 6.0, 6.0, 3.0, 3.0]
    
    print(lstsq(a, b)[0])

"""Main execution."""
if __name__ == "__main__":
    main()