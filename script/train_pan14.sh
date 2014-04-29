#!/bin/bash

traindir=
lang=all
genre=all
model=.

echo "Running training authorid"
while getopts i:l:g:o: opt; do
	case $opt in
	i)
		traindir=$OPTARG
		;;
	o)
		modeldir=$OPTARG
		;;
	esac
done

python src/authorid_sparse.py -m train --model ${modeldir}/sparse_authorid.model ${traindir} ${traindir}/truth.txt 
python src/authorid_imposter.py -m train --model ${modeldir}/imposter_authorid.model ${traindir} ${traindir}/truth.txt 
python src/authorid_bayes.py -m train --model ${modeldir}/bayes_authorid.model ${traindir} ${traindir}/truth.txt 

