#!/bin/bash
echo "Reading" $1
treetaggerdutch=treetager/cmd/tree-tagger-dutch
for d in $(ls -d $1/*/); do
  for i in $(ls $d); do
    cat $d$i | $treetaggerdutch > $d$i\_tag
  done;
done;
