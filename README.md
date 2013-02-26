authorid
========

Author identification code

Instrucctions for running in PAN13
----------------------------------

### Trainning assesment

  sh script/train_pan13.sh /media/pan13-training-data/pan13-author-identification-training-data/ /media/pan13-training-data/pan13-author-identification-training-data/Answers.txt


## Test on unknown data

  sh script/test_pan13.sh $DIR
  

### Development assesment

  sh script/develop_pan13.sh /media/pan13-training-data/pan13-author-identification-training-data/ /media/pan13-training-data/pan13-author-identification-training-data/Answers.txt


Requirements
------------

* python 2.7
* numpy, scikit
* scikit-learn
* python-cvxopt 

Optional:

* PAN dataset


Documentation
-------------

Create the documentation with makefile
  
   make doc


