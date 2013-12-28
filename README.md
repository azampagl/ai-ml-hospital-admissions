# Hospital Admission Machine Learning #

This is the top level directory for the application. Each sub-directory contains a README with the respective information for that directory.

## File Structure ##

* **data**

  The original data provided by the hospital. The data is **not** saved to the repository!

* **data-generator**

  Generates multi-dimensional linear data with an optional amount of normally distributed noise.

* **experiment**

  Experimentation with altnernative algorithms, such as Support Vector Machines (SVM).
	
* **feature-extractor**

  Python application that reads in the original hospital data and extracts the feature sets.

* **production**

  Contains the production C++ code for the final implementation of the RKGERS algorithm.

* **prototype**

  Experiment different approaches to the RKGERS algorithm.
	
* **results**

  Results from various algorithms applied to different data sets.

* **tmp**

  Blank directory used for temporary files. **No** data is contained in this folder.
