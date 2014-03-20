#!/bin/bash


if [ $# -lt 2 ]
then
	echo "Usage: `basename $0` InputDirectory OutputDirectory"
	echo "For extra options look at authorid.py script or README file"
	exit 1
fi
len=$(($#-2))
python src/authorid_bayes.py ${@:1:$len} ${@: -2} > ${@: -1}/answers_bayes.txt
echo "Saving results to" ${@: -1}/answers_bayes.txt
