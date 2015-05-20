#!/bin/bash

traindir=
genre=all
model=.

echo "Running training authorid"
while getopts i:l:g:o: opt; do
	case $opt in
	i)
		traindir=$OPTARG
		;;
	o)
		outdir=$OPTARG
		;;
	esac
done

echo "Developing"
python src/authorid.py -m devel -v -r bigrampref -r bigramsuf -r bigram -r bow -r trigram -r prefix -r sufix -r punct   ${traindir} ${traindir}/truth.txt > ${traindir}/answers.txt

