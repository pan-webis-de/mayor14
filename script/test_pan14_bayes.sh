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

#python src/authorid_sparse.py -m test --model ${modeldir}/sparse_authorid.model -r bigrampref -r bigramsuf -r bigram -r bow -r trigram -r prefix -r sufix -r punct -r wordssntc -r stopwords -r bigramstop ${testdir} ${testdir} > ${outdir}/answers_sparse.txt
echo "python src/authorid_bayes.py -m test --model ~/bayes_authorid.model -r bigrampref -r bigramsuf -r trigram -r bigram -r bow  -r trigram -r prefix -r sufix -r punct -r wordssntc -r stopwords -r bigramstop ${testdir} ${testdir} > ${outdir}/answers.txt"
python src/authorid_bayes.py -m test --model ~/bayes_authorid.model -r bigrampref -r bigramsuf -r trigram -r bigram -r bow  -r trigram -r prefix -r sufix -r punct -r wordssntc -r stopwords -r bigramstop ${testdir} ${testdir} > ${outdir}/answers.txt
#python src/authorid_imposter.py -m test --model ${modeldir}/imposter_authorid.model -r bigrampref -r bigramsuf -r bigram -r bow -r trigram -r prefix -r sufix -r punct -r wordssntc -r stopwords -r bigramstop ${testdir} ${testdir} > ${outdir}/answers_imposter.txt
#python src/mix_answers.py ${outdir}/answers_sparse.txt ${outdir}/answers_bayes.txt ${outdir}/answers_imposter.txt > ${outdir}/answers.txt
#rm ${outdir}/answers_sparse.txt
#rm ${outdir}/ansers_imposter.txt
#rm ${outdit}/answer_bayes.txt

