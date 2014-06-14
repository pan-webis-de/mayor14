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

echo "python src/authorid_bayes.py -m test --model ${modeldir}/bayes_authorid.model -r bigrampref -r bigramsuf -r trigram -r bigram -r bow  -r trigram -r prefix -r sufix -r punct -r wordssntc -r stopwords -r bigramstop ${testdir} ${testdir} > ${outdir}/answers.txt"
python src/authorid_bayes.py -m test --model ${modeldir}/bayes_authorid.model -r bigrampref -r bigramsuf -r trigram -r bigram -r bow  -r trigram -r prefix -r sufix -r punct -r wordssntc -r stopwords -r bigramstop ${testdir} ${testdir} > ${outdir}/answers.txt

