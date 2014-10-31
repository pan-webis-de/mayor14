authorid
========

Author identification code using:

* Bayes
* Imposters
* Sparse representation
 


Instrucctions for running in PAN14
----------------------------------

### Trainning the three methodologies

  bash script/train_pan14.sh -i TRAINDIR -o MODELDIR 


## Test for bayes
  
  bash script/test_pan14_bayes.sh -i INPUTDIR -m MODELDIR -o OUTPUTDIR 
  
## Test for imposter

  bash script/test_pan14_imposter.sh -i INPUTDIR -m MODELDIR -o OUTPUTDIR 

## Test for sparse

  bash script/test_pan14_sparse.sh -i INPUTDIR -m MODELDIR -o OUTPUTDIR 


The results will be saved into $OUTDIR/anwers.txt


Scripts
-------

For more information run:

  python src/authorid_bayes.py -h
  python src/authorid_imposter.py -h
  python src/authorid_sparse.py -h

Requirements
------------

* python 2.7
* numpy, scikit
* scikit-learn
* python-cvxopt 
* oct2py


Install stanford libraries

:: 

  mkdir lib
  wget http://nlp.stanford.edu/software/stanford-corenlp-full-2014-08-27.zip
  unzip stanford-corenlp-full-2014-08-27.zip
  cp stanford-corenlp-full-2014-08-27/stanford-corenlp-3.4.1.jar lib/
  cp stanford-corenlp-full-2014-08-27/stanford-corenlp-3.4.1-models.jar lib/


Optional:

* PAN dataset

