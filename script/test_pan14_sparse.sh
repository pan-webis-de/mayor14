#!/bin/bash

testdir=
model=.

echo "Running testing authorid"
while getopts i:l:g:o:m: opt; do
	case $opt in
	i)
		testdir=$OPTARG
		;;
	m)
		modeldir=$OPTARG
		;;
	o)
		outdir=$OPTARG
		;;
	esac
done

echo "python src/authorid_sparse.py -m test --model ${modeldir}/sparse_authorid.model -r bigrampref -r bigramsuf -r bigram -r bow -r trigram -r prefix -r sufix -r punct -r wordssntc -r stopwords -r bigramstop ${testdir} ${testdir} > ${outdir}/answers_sparse.txt"
python src/authorid_sparse.py -m test --model ${modeldir}/sparse_authorid.model -r bigrampref -r bigramsuf -r bigram -r bow -r trigram -r prefix -r sufix -r punct -r wordssntc -r stopwords -r bigramstop ${testdir} ${testdir} > ${outdir}/answers_sparse.txt

