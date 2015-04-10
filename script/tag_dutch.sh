#!/bin/bash
echo "Reading" $1
treetaggerdutch=treetager/cmd/tree-tagger-dutch
for i in $(ls $1); do
  cat $1$i | $treetaggerdutch > $1$i\_tag
done;
