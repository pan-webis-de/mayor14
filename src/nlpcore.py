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


import  jpype 

jpype.startJVM(jpype.getDefaultJVMPath(),
    "-ea",
    "-Djava.class.path=lib/stanford-corenlp-3.4.1.jar:lib/stanford-corenlp-3.4.1-models.jar"
    )

class POS():
    def __init__(self,model="edu/stanford/nlp/models/pos-tagger/english-left3words/english-left3words-distsim.tagger"):
        MaxentTagger = jpype.JPackage("edu").stanford.nlp.tagger.maxent.MaxentTagger
        self.tagger = MaxentTagger(model)

    def tag(self,text):
        tag=self.tagger.tagString(text)
        tags=[wT.split('_',1)[1] for wT in tag.split()]
        return tags

    def close(self):
        jpype.shutdownJVM()

postagger = POS()
