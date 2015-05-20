#!/bin/bash
echo "Reading" $1
treetaggerdutch=script/treetager/cmd/tree-tagger-dutch
for d in $(ls -d $1/*/); do
  for i in $(ls $d/*.txt); do
	cat $i | $treetaggerdutch | awk -F, '{print $1,$3,$2}' OFS=\t > $i\_tag
  done;
done;
