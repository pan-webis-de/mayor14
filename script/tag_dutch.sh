#!/bin/bash
echo "Reading" $1
treetaggerdutch=script/treetager/cmd/tree-tagger-dutch
for i in $(ls $1/*.txt); do
  cat $i | $treetaggerdutch | awk -F, '{print $1,$3,$2}' OFS=\t  > $i\_tag
done;
