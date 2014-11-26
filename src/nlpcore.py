#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Binding to POS tagger for nlpcore from standford
# ----------------------------------------------------------------------
# Ivan Vladimir Meza-Ruiz/ ivanvladimir at turing.iimas.unam.mx
# 2014/IIMAS/UNAM
# ----------------------------------------------------------------------
# nlpcore_pos.py is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# -------------------------------------------------------------------------


from nltk.stem import SpanishStemmer
import  jpype 

jpype.startJVM(jpype.getDefaultJVMPath(),
    "-ea",
    "-Djava.class.path=lib/stanford-corenlp-3.4.1.jar:lib/stanford-corenlp-3.4.1-models.jar:lib/stanford-spanish-corenlp-2014-08-26-models.jar"
    )

def close():
    jpype.shutdownJVM()
    

class POS_lemma_es():
    def __init__(self,model="edu/stanford/nlp/models/pos-tagger/spanish/spanish-distsim.tagger"):
        self.StringReader = jpype.JPackage("java").io.StringReader
        self.CoreLabelTokenFactory =\
            jpype.JPackage("edu").stanford.nlp.process.CoreLabelTokenFactory
        self.SpanishTokenizer =\
            jpype.JPackage("edu").international.spanish.process.SpanishTokenizer
        WordToSentenceProcessor =\
            jpype.JPackage("edu").stanford.nlp.process.WordToSentenceProcessor
        MaxentTagger = jpype.JPackage("edu").stanford.nlp.tagger.maxent.MaxentTagger
        self.postagger  = MaxentTagger(model)
        self.stemmer    = SpanishStemmer()
        self.ssplit     = WordToSentenceProcessor()


    def tag(self,text):
        text_=self.StringReader(text.encode("ascii","ignore"))
        tokenizer = self.SpanishTokenizer(text_,self.CoreLabelTokenFactory(),"invertible,ptb3Escaping=truei,splitAll=True")
        tokens=tokenizer.tokenize()
        sntcs=self.ssplit.process(tokens)
        labels=[]
        for sntc in sntcs:
            pos=self.postagger.tagSentence(sntc)
            for wt in pos:
                lemma=self.stem(wt.word())
                labels.append((wt.word(),wt.tag(),lemma))
        return labels,text.encode('utf-8')

class POS_lemma():
    def __init__(self,model="edu/stanford/nlp/models/pos-tagger/english-left3words/english-left3words-distsim.tagger"):
        self.StringReader = jpype.JPackage("java").io.StringReader
        self.CoreLabelTokenFactory =\
            jpype.JPackage("edu").stanford.nlp.process.CoreLabelTokenFactory
        self.PTBTokenizer =\
            jpype.JPackage("edu").stanford.nlp.process.PTBTokenizer
        WordToSentenceProcessor =\
            jpype.JPackage("edu").stanford.nlp.process.WordToSentenceProcessor
        MaxentTagger = jpype.JPackage("edu").stanford.nlp.tagger.maxent.MaxentTagger
        Morphology = \
            jpype.JPackage("edu").stanford.nlp.process.Morphology
        self.postagger  = MaxentTagger(model)
        self.lemmatizer = Morphology()
        self.ssplit     = WordToSentenceProcessor()


    def tag(self,text):
        text_=self.StringReader(text.encode("ascii","ignore"))
        tokenizer = self.PTBTokenizer(text_,self.CoreLabelTokenFactory(),"invertible,ptb3Escaping=true")
        tokens=tokenizer.tokenize()
        sntcs=self.ssplit.process(tokens)
        labels=[]
        for sntc in sntcs:
            pos=self.postagger.tagSentence(sntc)
            for wt in pos:
                lemma=self.lemmatizer.lemma(wt.word(),wt.tag())
                labels.append((wt.word(),wt.tag(),lemma))
        return labels,text.encode("utf-8")


class POS():
    def __init__(self,model="edu/stanford/nlp/models/pos-tagger/english-left3words/english-left3words-distsim.tagger"):
        MaxentTagger = jpype.JPackage("edu").stanford.nlp.tagger.maxent.MaxentTagger
        self.tagger = MaxentTagger(model)

    def tag(self,text):
        tag=self.tagger.tagString(text)
        tags=[wT.split('_',1)[1] for wT in tag.split()]
        return tags

class lemma():
    def __init__(self,model="edu/stanford/nlp/models/pos-tagger/english-left3words/english-left3words-distsim.tagger"):
        MaxentTagger = jpype.JPackage("edu").stanford.nlp.tagger.maxent.MaxentTagger
        self.tagger = MaxentTagger(model)

    def tag(self,text):
        tag=self.tagger.tagString(text)
        tags=[wT.split('_',1)[1] for wT in tag.split()]
        return tags,text


postagger = POS()
fulltagger = POS_lemma()
