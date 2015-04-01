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
from __future__ import print_function

# System libraries
import argparse
import sys
import os
import os.path
import cmd
import random
import json
from oct2py import octave
octave.addpath('src/octave')

# Local imports
import docread
import hbc

out=sys.stdout

def info(*args):
    """ Function to print info"""
    print(*args,file=out)

class AuthorIdCLI(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.promtp = "> "
        self.intro  = "Welcome to the authorid  console!"
        self.doc    = 0
        self.max    = 100
        self.id2doc = dict([(problem[0],i) for i,problem in enumerate(problems)])

    def do_next(self,args):
        "Move to the next document"
        self.doc+=1
        if self.doc > len(problems):
            self.doc=0
        print("In problem:", problems[self.doc][0])

    def do_prev(self,args):
        "Move to the previous document"
        self.doc-=1
        if self.doc < 0:
            self.doc=0
        print("In problem:", problems[self.doc][0])



    def do_next_error(self,args):
        "Move to tne next document"
        error=False
        if not sy:
            print("Error: No system predictions loaded")
            return
        while not error and self.doc<len(problems):
            self.doc+=1
            if gs[problems[self.doc][0]]=='Y' and sy[problems[self.doc][0]]<0.5:
                error=True
            elif gs[problems[self.doc][0]]=='N' and sy[problems[self.doc][0]]>0.5:
                error=True
            elif sy[problems[self.doc][0]]==0.5:
                error=True


        if self.doc == len(problems):
            self.doc=0
            print("error: reached last problem")
            return 
        print("In problem:", problems[self.doc][0])


    def do_gs_answer(self,args):
        "Shows the goldstandard answer of the problem"
        print("Answer          : ", gs[problems[self.doc][0]])

    def do_reloadfeats(self,args):
        "Reload representations"
        import docread
        docread = reload(docread)


    def do_sys_answer(self,args):
        "Shows the answer of the problem"
        if sy:
            print("Predction       : ", sy[problems[self.doc][0]])
        else:
            print("No prediction loadded error")

    def do_pred(self,args):
        "Predicts the answer"
        args=self.parse(args)
        if len(args)==0:
            reps=list(set(opts.reps))
        else:
            reps=list(set(opts.reps+args))
        opts.reps=reps
        hbc.process_corpus([problems[self.doc]],
                impostors,opts=opts,sw=stopwords,verbose=verbose)
        
    def do_info(self,args):
        "Shows info of the problem"
        print("Problem Id      : ", problems[self.doc][0])
        print("Known documents : ", len(problems[self.doc][1][0]))
        print("Answer          : ", gs[problems[self.doc][0]])
        if sy:
            print("Predction       : ", sy[problems[self.doc][0]])
        print("Known files     : ",len(problems[self.doc][1][0]))
        print("Unknown file    : ",len(problems[self.doc][1][1]))

            
    def do_current(self,args):
        "Shows the id of the current problem"
        print("Problem Id      : ", problems[self.doc][0])

    def do_dump(self,args):
        "Prints document by its index (use info to print indexes)"
        
        lks= len(problems[self.doc][1][0])
        args=self.parse(args)
        if len(args)==0:
            args=range(lks+1)
        for i in args:
            try:
                i=int(i)
            except ValueError:
                print("error: invalid index has to be number",i)
                return
        
            if i+1 > lks:
                print("===> Unknown document ({0})".format(i))
                try:
                    for line in open("{1}".format(
                                    opts.GS,
                                    problems[self.doc][1][1][i-lks][0])):
                        line = line.strip()
                        print(line)
                except IndexError:
                    print("error: no document with that index",i)
                    return
            else:
                print("===> known document ({0})".format(i))
                for line in open("{1}".format(
                                    opts.GS,problems[self.doc][1][0][i][0])):
                    print(line)
        print("Done.")

    def do_tag(self,args):
        "Prints tags for document by its index (use info to print indexes)"
        
        lks= len(problems[self.doc][1][0])
        args=self.parse(args)
        if len(args)==0:
            args=range(lks+1)
        for i in args:
            try:
                i=int(i)
            except ValueError:
                print("error: invalid index has to be number",i)
                return
        
            if i+1 > lks:
                print("===> Unknown document ({0})".format(i))
                try:
                    doc=problems[self.doc]
                    doc,text=docread.tag(doc[1][1][i-lks][0],doc[1][1][i-lks][1],opts.language)
                    data = [ u"{0}/{1}".format(x,y) for x,y,z in 
                                    doc]
                    line = " ".join(data)
                    print(line)
                except IndexError:
                    print("error: no document with that index",i)
                    return
            else:
                print("===> known document ({0})".format(i))
                doc=problems[self.doc]
                doc,text=docread.tag(doc[1][0][i-lks][0],doc[1][0][i-lks][1],opts.language)
                data = [ u"{0}/{1}".format(x,y) for x,y,z in 
                                    doc]
                line = " ".join(data)
                print(line)
            
            print("Done.")



    def __do_print(self,args):
        "Prints document by its index (use info to print indexes)"
        
        lks= len(problems[self.doc][1][0])
        args=self.parse(args)
        if len(args)==0:
            args=range(lks+1)
        for i in args:
            try:
                i=int(i)
            except ValueError:
                print("error: invalid index has to be number",i)
                return
        
            if i+1 > lks:
                print("===> Unknown document ({0})".format(i-lks))
                try:
                    print(u"".join([x[0] for x in
                        problems[self.doc][1][1][i-lks][1]]))
                except IndexError:
                    print("error: no document with that index",i)
                    return
            else:
                print("===> known document ({0})".format(i))
                print(u"".join([x[0] for x in
                            problems[self.doc][1][0][i][1]]))
        print("Done.")

    def do_show(self,args):
        """Shows document in some representation
        show ngram 0
        show ngram
        """
        
        lks= len(problems[self.doc][1][0])
        args=self.parse(args)
        if not len(args)>=1:
            print("error: enough arguments")
            return
        try:
            exec("f=docread.{0}".format(args[0]))
        except:
            print("error: not representation available")
            return
        if len(args)==1:
            args=range(lks+1)
        else:
            args=args[1:]


        for i in args:
            try:
                i=int(i)
            except ValueError:
                print("error: invalid index has to be number",i)
                return
        
            if i+1 > lks:
                print("===> Unknown document ({0})".format(i))
                try:
                    doc=problems[self.doc]
                    doc,text=docread.tag(doc[1][1][i-lks][0],doc[1][1][i-lks][1],opts.language)
                    rep=f(doc,text,sw=stopwords,cutoff=opts.cutoff)
                    printrep(rep,self.max)
                except IndexError:
                    print("error: no document with that index",i)
                    return
            else:
                print("===> known document ({0})".format(i))
                doc=problems[self.doc]
                doc,text=docread.tag(doc[1][0][i][0],doc[1][0][i][1],opts.language)
                rep=f(doc,text,sw=stopwords)
                printrep(rep,self.max)
        print("Done.")



    def do_go(self,args):
        """Goes to a specif problem
           go EN001
        """
        
        args=self.parse(args)
        if len(args)==1:
            try:
                self.doc=self.id2doc[args[0]]
                print("Problem Id      : ", problems[self.doc][0])
                print("Done")
            except KeyError:
                print("error: id does not exists")
        else:
            print("error: too many ids")

    def do_reps(self, arg):
        'List availablre representations'
        for rep in docread.representations:
            print(rep[0])
        print("Done.")



    def do_bye(self, arg):
        'Exit'
        return True

    def parse(self,args):
        return args.split()

    
 

def printrep(c,nmost=1000):
    vals=c.most_common()[:nmost]
    print("Total classes:", len(c))
    print("Total mass   :", sum(c.values()))
    for i in range(len(vals)/5+1):
        print(u" | ".join([u"{0:<10}:{1:>3}".format(x[:10],v) for x,v in
            vals[(i*5):(i*5)+5]]))


codes=docread.codes

# MAIN program
if __name__ == "__main__":

    # Command line options
    p = argparse.ArgumentParser("Author identification")
    p.add_argument("DIR",default=None,
            action="store", help="Directory with examples")
    p.add_argument("GS",default=None,
            action="store", help="File with the truth answers")
    p.add_argument("SYS",default=None,nargs='?',
            action="store", help="File with the predicted answers")
    p.add_argument("--cutoff",default=2,type=int,
            action="store", dest="cutoff",
            help="Minimum frequency [5]")
    p.add_argument("-r","--rep",default=['bow','bigram'],
            action="append", dest="reps",
            help="adds representation to process")
    p.add_argument("--iters",default=35,type=int,
            action="store", dest="iters",
            help="Total iterations [35]")
    p.add_argument("--impostors",default=None,
            action="store", dest="impostors",
            help="Directory of imposter per auhtor")
    p.add_argument("--max",default=0,type=int,
            action="store", dest="nmax",
            help="Maximum number of problems to solve [All]")
    p.add_argument("--nimpostors",default=8,type=int,
            action="store", dest="nimpostors",
            help="Total of imposter per auhtor [8]")
    p.add_argument("--documents",default=1,type=int,
            action="store", dest="ndocs",
            help="Documents per author [1]")
    p.add_argument("--percentage",default=.80,type=float,
            action="store", dest="percentage",
            help="Sampling percentage [.80]")
    p.add_argument("--stopwords", default=None,
            action="store", dest="stopwords",
            help="List of stop words [None, uses default]")
    p.add_argument("--genre",default='all',
            action="store", dest="genre",
            help="Genre to process [all]")
    p.add_argument('--version', action='version', version='%(prog)s 0.2')
    p.add_argument("-v", "--verbose",
            action="store_true", dest="verbose",
            help="Verbose mode [Off]")
    opts = p.parse_args()

    # prepara función de verbose
    if opts.verbose:
        def verbose(*args,**kargs):
            print(*args,**kargs)
    else:   
        verbose = lambda *a: None 
    opts.dump=False

    # Managing configurations  --------------------------------------------
    # Parameters
    # Patterns for files
    #
    known_pattern=r'known.*\.txt$'
    unknown_pattern=r'unknown*.txt$'

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

    # Loading language
    with open("{0}/{1}".format(opts.DIR,'contents.json')) as data_file:    
        jinfo = json.load(data_file)
    if jinfo['language'].startswith('Dutch'):
        opts.language="nl"
    if jinfo['language'].startswith('Espanish'):
        opts.language="es"
    if jinfo['language'].startswith('English'):
        opts.language="en"
    if jinfo['language'].startswith('Greek'):
        opts.language="gr"

    # Loading stopwords if exits
    stopwordspat="data/stopwords_{0}.txt"
    stopwords=[]
    if not opts.stopwords:
        fstopwords=stopwordspat.format(docread.codes[opts.language]['stopwords'])
    else:
        fstopwords=opts.stopwords
    if os.path.exists(fstopwords):
        verbose('Loading stopwords: ',fstopwords)
        stopwords=docread.readstopwords(fstopwords)
    else:
        info('Stopwords file',fstopwords,' not found assuming emtpy',opts.stopwords)

    # Loading main files -------------------------------------------------
    # load problems or problem
    verbose('Loading files')
    problems=docread.problems(
             docread.dirproblems(opts.DIR,known_pattern,unknown_pattern,_ignore,
                                 code=docread.codes[opts.language][opts.genre]))
    verbose('Finish loading files')
    verbose('Total problems',len(problems))

    # load impostors from directory
    impostors=None
    if opts.impostors:
        impostors=[]
        verbose('Loading impostors')
        files  =[(i,x,os.path.join(opts.impostors,x)) for i,x in
                                enumerate(os.listdir(opts.impostors))
                                if x.endswith(".txt")]
        random.shuffle(files)
        for i,id,f in files:
                impostors.append(
                    (opts.impostors[-2:]+"__"+str(i),
                    ([(f,docread.readdoc(f))],[])))
    else:
        verbose('Using problems as impostors')
        impostors=problems
    verbose('Total impostors',len(impostors))

    gs = docread.loadanswers(opts.GS,code=codes[opts.language][opts.genre])
    sy=None
    if opts.SYS:
        sy = docread.loadanswers(opts.SYS,code=codes[opts.language][opts.genre])
  

    console=AuthorIdCLI()
    console.cmdloop()
