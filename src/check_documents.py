#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Checking documents
# ----------------------------------------------------------------------
# Ivan V. Meza
# 2014/IIMAS, México
# ----------------------------------------------------------------------
# authorid_sparse.py is free software: you can redistribute it and/or modify
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

# System libraries
import argparse
import sys
import os
import os.path
import sklearn.preprocessing as preprocessing
import numpy as np
import random
import itertools
import cmd
from collections import Counter
from oct2py import octave
octave.addpath('src/octave')

# Local imports
import docread

def verbose(*args):
    """ Function to print verbose"""
    if opts.verbose:
        print >> out, "".join(args)

def info(*args):
    """ Function to print info"""
    print >> out, "".join(args)


class AuthorIdCLI(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.promtp = "> "
        self.intro  = "Welcome to the authorid  console!"
        self.doc    = 0
        self.max    = 100
        self.id2doc = dict([(problem[0],i) for i,problem in enumerate(problems)])

    def do_next(self,args):
        "Move to tne next document"
        self.doc+=1
        if self.doc > len(problems):
            seld.doc=0
        print "In problem:", problems[self.doc][0]

    def do_next_error(self,args):
        "Move to tne next document"
        error=False
        while not error and self.doc<len(problems):
            self.doc+=1
            if gs[problems[self.doc][0]]=='Y' and sys[problems[self.doc][0]]<0.5:
                error=True
            elif gs[problems[self.doc][0]]=='N' and sys[problems[self.doc][0]]>0.5:
                error=True
            elif sys[problems[self.doc][0]]==0.5:
                error=True


        if self.doc == len(problems):
            seld.doc=0
            print "error: reached last problem"
            return 
        print "In problem:", problems[self.doc][0]


    def do_answer(self,args):
        "Shows the answer of the problem"
        print "Answer          : ", gs[problems[self.doc][0]]


    def do_pred(self,args):
        "Shows the prediction of the problem"
        print "Predction       : ", sys[problems[self.doc][0]]



    def do_info(self,args):
        "Shows info of the problem"
        print "Problem Id      : ", problems[self.doc][0]
        print "Known documents : ", len(problems[self.doc][1][0])
        print "Answer          : ", gs[problems[self.doc][0]]
        print "Predction       : ", sys[problems[self.doc][0]]
        print "Known files     : "
        for i,doc in enumerate(problems[self.doc][1][0]):
            bow=docread.bow(doc[1])[0]
            print "    [{0}]".format(i), doc[0], "({0})".format(sum(bow.values()))
        print "Unknown file   : "
        for doc in problems[self.doc][1][1]:
            i+=1
            bow=docread.bow(doc[1])[0]
            print  "    [{0}]".format(i),doc[0],"({0})".format(sum(bow.values()))
            
    def do_current(self,args):
        "Shows the id of the current problem"
        print "Problem Id      : ", problems[self.doc][0]
 
    def do_print(self,args):
        "Prints document by its index (use info to print indexes)"
        
        lks= len(problems[self.doc][1][0])
        args=self.parse(args)
        if len(args)==0:
            args=range(lks+1)
        for i in args:
            try:
                i=int(i)
            except ValueError:
                print "error: invalid index has to be number",i
                return
        
            if i+1 > lks:
                print "===> Unknown document ({0})".format(i)
                try:
                    print problems[self.doc][1][1][i-lks][1]
                except IndexError:
                    print "error: no document with that index",i
                    return
            else:
                print "===> known document ({0})".format(i)
                print problems[self.doc][1][0][i][1]
        print "Done."

    def do_show(self,args):
        """Shows document in some representation
        show ngram 0
        show ngram
        """
        
        lks= len(problems[self.doc][1][0])
        args=self.parse(args)
        if not len(args)>0:
            print "error: enough arguments"
        exec("f=docread.{0}".format(args[0]))
        if len(args)==1:
            args=range(lks+1)


        for i in args:
            try:
                i=int(i)
            except ValueError:
                print "error: invalid index has to be number",i
                return
        
            if i+1 > lks:
                print "===> Unknown document ({0})".format(i)
                try:
                    rep=f(problems[self.doc][1][1][i-lks][1],sw=stopwords)
                    printrep(rep[0],self.max)
                except IndexError:
                    print "error: no document with that index",i
                    return
            else:
                print "===> known document ({0})".format(i)
                rep=f(problems[self.doc][1][0][i][1],sw=stopwords)
                printrep(rep[0],self.max)
        print "Done."



    def do_go(self,args):
        """Goes to a specif problem
           go EN001
        """
        
        args=self.parse(args)
        if len(args)==1:
            try:
                self.doc=self.id2doc[args[0]]
                print "Problem Id      : ", problems[self.doc][0]
                print "Done"
            except KeyError:
                print "error: id does not exists"
        else:
            print "error: too many ids"

    def do_reps(self, arg):
        'List availablre representations'
        for rep in docread.representations:
            print rep[0]
        print "Done."



    def do_bye(self, arg):
        'Exit'
        return True

    def parse(self,args):
        return args.split()

    
 

def printrep(c,nmost=1000):
    vals=c.most_common()[:nmost]
    print "Total classes:", len(c)
    print "Toral mass   :", sum(c.values())
    for i in range(len(vals)/5):
        print " | ".join(["{0:<10}:{1:>3}".format(x[:10],v) for x,v in vals[(i*5):(i*5)+5]])


codes=docread.codes

# MAIN program
if __name__ == "__main__":

    # Command line options
    p = argparse.ArgumentParser("Author identification")
    p.add_argument("DIR",default=None,
            action="store", help="Directory with examples")
    p.add_argument("GS",default=None,
            action="store", help="File with the truth answers")
    p.add_argument("SYS",default=None,
            action="store", help="File with the predicted answers")
    p.add_argument("--stopwords", default="data/stopwords.txt",
            action="store", dest="stopwords",
            help="List of stop words [data/stopwords.txt]")
    p.add_argument("--language",default='all',
            action="store", dest="language",
            help="Language to process [all]")
    p.add_argument("--genre",default='all',
            action="store", dest="genre",
            help="Genre to process [all]")
    p.add_argument('--version', action='version', version='%(prog)s 0.2')
    p.add_argument("-v", "--verbose",
            action="store_true", dest="verbose",
            help="Verbose mode [Off]")
    opts = p.parse_args()

    #if not opts.random:
    #    random.seed(9111978)

    # Managing configurations  --------------------------------------------
    # Parameters
    # Patterns for files
    known_pattern=r'known.*\.txt'
    unknown_pattern=r'unknown*.txt'

    dirname = opts.DIR

    # Loading configuration files ----------------------------------------
    # - .ignore   : files to ignore some files
    # - stopwords : words to ignore from the documents

    # Loading ignore if exists
    _ignore=[]
    if os.path.exists('.ignore'):
        verbose('Loading files to ignore from: .ignore')
        with open('.ignore') as file:
            for line in file:
                _ignore.append(line.strip())


    # Loading stopwords if exits
    stopwords=[]
    if os.path.exists(opts.stopwords):
        verbose('Loading stopwords: ',opts.stopwords)
        stopwords=docread.readstopwords(opts.stopwords)
    else:
        info('Stopwords file not found assuming, emtpy',opts.stopwords)

    # Loading main files -------------------------------------------------
    # load problems or problem
    verbose('Loading files')
    problems=docread.problems(
             docread.dirproblems(dirname,known_pattern,unknown_pattern,_ignore,
                                 code=codes[opts.language][opts.genre]))
        
    gs = docread.loadanswers(opts.GS,code=codes[opts.language][opts.genre])
    sys = docread.loadanswers(opts.SYS,code=codes[opts.language][opts.genre])
  

    console=AuthorIdCLI()
    console.cmdloop()
