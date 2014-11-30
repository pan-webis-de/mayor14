#!/bin/bash

diez=10
for PER in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
do
	python src/authorid_sparse.py --percentage ${PER} --nimpostors 2 -m devel --impostors data/imposters/EE --dumpfiles -r punct -r nstcs data/pan14_train/pan14-author-verification-training-corpus-english-essays-2014-04-22 data/pan14_train/pan14-author-verification-training-corpus-english-essays-2014-04-22/truth.txt > data/pan14_train/pan14-author-verification-training-corpus-english-essays-2014-04-22/answers_all.txt
	dir="final/ee_2i_punct_nstcs_${PER}"
	echo $dir
	mkdir $dir
	cp answers*.dump $dir
	cp data/pan14_train/pan14-author-verification-training-corpus-english-essays-2014-04-22/answers_all.txt $dir
done
