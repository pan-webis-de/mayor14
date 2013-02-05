#!/bin/bash

echo "Positive evaluation"
python src/authorid.py data/palacio_valdes/ data/palacio_valdes_pos.txt

echo "Negative evaluation"
python src/authorid.py data/palacio_valdes/ data/palacio_valdes_neg.txt
 
