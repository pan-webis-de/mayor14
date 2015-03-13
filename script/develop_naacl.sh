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
		outdir=$OPTARG
		;;

	esac
done

echo "Developing"
python src/authorid_sparse.py -m devel -r bigrampref -r bigramsuf -r bigram -r bow -r trigram -r prefix -r sufix -r punct -r wordssntc -r stopwords -r bigramstop ${traindir} ${traindir}/truth.txt > ${traindir}/answers.txt

