#!/bin/bash

echo "Running training pan"
python src/authorid.py  -m train -v data/PAN13-AuthorIdentification-TrainingCorpus data/PAN13-AuthorIdentification-TrainingCorpus/Answers.txt
