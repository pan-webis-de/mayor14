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
	l)
		lang=$OPTARG
		;;
	g)
		genre=$OPTARG
		;;
	o)
		model=$OPTARG
		;;
	esac
done


python src/authorid.py -m train --language ${lang} --genre ${genre} --model ${model}/${lang}_${genre}_authorid.model ${traindir} ${traindir}/truth.txt 
