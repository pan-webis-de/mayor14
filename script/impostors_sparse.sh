#!/bin/bash

diez=10
for IMP in 5 6 7 8
do
	python src/authorid_sparse.py --nimpostors ${IMP} --lang es -m devel --impostors data/imposters/SP --dumpfiles -r poslemma -r ngrampos -r ngramword -r capital -r numbers -r punct -r bow -r lemma -r pos -r nstcs data/pan14_train/pan14-author-verification-training-corpus-spanish-articles-2014-04-22 data/pan14_train/pan14-author-verification-training-corpus-spanish-articles-2014-04-22/truth.txt > data/pan14_train/pan14-author-verification-training-corpus-spanish-articles-2014-04-22/answers_all.txt
	dir="final/sp_capital_numbers_punct_bow_lema_pos_nstcs_impostors_${IMP}"
	echo $dir
	mkdir $dir
	cp answers*.dump $dir
	cp data/pan14_train/pan14-author-verification-training-corpus-spanish-articles-2014-04-22/answers_all.txt $dir
done
