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

echo "First stage"
#python src/authorid_sparse.py -m devel -r bigrampref -r bigramsuf -r bigram -r bow -r trigram -r prefix -r sufix -r punct -r wordssntc -r stopwords -r bigramstop ${traindir} ${traindir}/truth.txt > ${traindir}/answers_sparse.txt
echo "Second stage"
#python src/authorid_imposter.py -m devel -r bigrampref -r bigramsuf -r bigram -r bow -r trigram -r prefix -r sufix -r punct -r wordssntc -r stopwords -r bigramstop ${traindir} ${traindir}/truth.txt > ${traindir}/answers_imposter.txt
echo "Third stage"
python src/authorid_bayes.py -m devel ${traindir} ${traindir}/truth.txt > ${traindir}/answers_bayes.txt 
echo "Creating answers"
python src/mix_answers.py ${outdir}/answers_sparse.txt ${outdir}/answers_bayes.txt ${outdir}/answers_imposter.txt > ${outdir}/answers.txt
#rm ${output}/sparse_answers.txt
#rm ${output}/imposter_answers.txt
#rm ${output}/bayes_answers.txt

