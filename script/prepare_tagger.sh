#!/bin/bash

mkdir lib
cd lib
ls
wget http://nlp.stanford.edu/software/stanford-corenlp-full-2015-01-29.zip
unzip stanford-corenlp-full-2015-01-29.zip
wget http://nlp.stanford.edu/software/stanford-spanish-corenlp-2015-01-08-models.jar
cd ../src/java

javac -classpath ../../lib/*:. SpanishTagger.java
javac -classpath ../../lib/*:. EnglishTagger.java

java -classpath ../../lib/*: SpanishTagger ../../data/pan15_train/spanish
java -classpath ../../lib/*: EnglishTagger ../../data/pan15_train/english
