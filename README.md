authorid
========

Author identification code

Instrucctions for running in PAN13
----------------------------------

### Trainning assesment

  bash script/train_pan13.sh TRAINDIR 


## Test on unknown data

  bash script/test_pan13.sh INPUTDIR OUTPUTDIR
  
The results will be saved into $OUTDIR/Results.txt


### Development assesment

  bash script/develop_pan13.sh TRAINDIR


Requirements
------------

* python 2.7
* numpy, scikit
* scikit-learn
* python-cvxopt 
* pybrain

Optional:

* PAN dataset


Documentation
-------------

Create the documentation with makefile
  
   make doc


