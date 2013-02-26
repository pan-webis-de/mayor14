#!/bin/bash

echo "Running training authorid"
python src/authorid.py -m train  $*
