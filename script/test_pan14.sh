#!/bin/bash

traindir=
lang=all
genre=all
model=pan14.model

echo "Running training authorid"
while getopts i:l:g:o:m: opt; do
	case $opt in
	i)
		testdir=$OPTARG
		;;
	l)
		lang=$OPTARG
		;;
	g)
		genre=$OPTARG
		;;
	m)
		model=$OPTARG
		;;
	o)
		outdir=$OPTARG
		;;
	esac
done


python src/authorid.py -m test --language ${lang} --genre ${genre} --model ${model} ${testdir} ${testdir} > ${outdir}/answers.txt
