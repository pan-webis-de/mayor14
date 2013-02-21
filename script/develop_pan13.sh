#!/bin/bash

echo "Running development authorid"
python src/authorid.py  -m devel -v $* data/PAN13-AuthorIdentification-TrainingCorpus data/PAN13-AuthorIdentification-TrainingCorpus/Answers.txt
