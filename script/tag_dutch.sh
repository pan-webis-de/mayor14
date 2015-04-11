#!/bin/bash
echo "Reading" $1
treetaggerdutch=script/treetager/cmd/tree-tagger-dutch
for i in $(ls $1); do
  cat $1$i | $treetaggerdutch | awk -F, '{print $1,$3,$2}' OFS=\t  > $1$i\_tag
done;
