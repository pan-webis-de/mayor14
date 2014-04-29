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

python src/authorid_sparse.py -m test --model ${model} ${testdir} ${testdir} > ${outdir}/sparse_answers.txt
python src/authorid_imposter.py -m test --model ${model} ${testdir} ${testdir} > ${outdir}/imposter_answers.txt
#python src/authorid_bayes.py -m test --model ${model}  ${testdir} ${testdir} > ${outdir}/bayes_answers.txt
pytho src/mix_answers ${outdir}/sparse_answers.txt ${outdir} ${outdir}/imposter_answers.txt > ${outdir}/answers.txt
#rm ${output}/sparse_answers.txt
#rm ${output}/imposter_answers.txt
#rm ${output}/bayes_answers.txt

