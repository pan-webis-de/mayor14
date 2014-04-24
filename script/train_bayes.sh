#!/bin/bash
#para probrar: bash script/train_bayes.sh

traindir=data/pan14-train


python src/authorid_bayes.py -m train --model ./authorid_bayes.model ${traindir} ${traindir}/truth.txt 
