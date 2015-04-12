#!/bin/bash

testdir=
model=.

echo "Running testing authorid"
while getopts i:o:m: opt; do
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

LANG=`cat ${testdir}/contents.json | grep language`
echo $LANG

if [[ $LANG == *"English"* ]]
then
	bash script/tag_train_english.sh ${testdir}
	python src/authorid.py -m test -r ngrampos -r ngramlemma -r gram8letter --lang en --impostors data/imposters2015/EN ${testdir}  > ${outdir}/answers.txt
fi
if [[ $LANG == *"Spanish"* ]]
then
	bash script/tag_train_spanish.sh ${testdir}
	python src/authorid.py -m test -r ngrampos -r ngramlemma -r gram8letter --lang es --impostors data/imposters2015/SP ${testdir}  > ${outdir}/answers.txt
fi
if [[ $LANG == *"Greek"* ]]
then
	python src/authorid.py -m test -r ngrampos --lang gr --impostors data/imposters2015/GR ${testdir} > ${outdir}/answers.txt
fi
if [[ $LANG == *"Dutch"* ]]
then
	bash script/tag_train_dutch.sh ${testdir}
	python src/authorid.py -m test --lang du --impostors data/imposters2015/DU ${testdir}  > ${outdir}/answers.txt
fi

