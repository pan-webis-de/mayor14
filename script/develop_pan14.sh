#!/bin/bash

traindir=
lang=all
genre=all
model=pan14.model
ansfile=truth.txt

echo "Running training authorid"
while getopts i:l:g:o:a: opt; do
	case $opt in
	i)
		traindir=$OPTARG
		;;
	l)
		lang=$OPTARG
		;;
	g)
		genre=$OPTARG
		;;
	a)	
		ansfile=$OPTARG
		;;
	esac
done


python src/authorid.py --verbose -m devel --language ${lang} --genre ${genre} ${traindir} ${traindir}/${ansfile}
