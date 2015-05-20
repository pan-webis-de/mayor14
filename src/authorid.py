#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Author ID main using a sparse representation
# ----------------------------------------------------------------------
# Ivan V. Meza
# 2014/IIMAS, México
# ----------------------------------------------------------------------
# authorid.py is free software: you can redistribute it and/or modify
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
import random
import json
from oct2py import octave
# Local imports
import docread
import hbc
import config

octave.addpath('src/octave')
octave.timeout=60


out=sys.stdout

def info(*args):
    """ Function to print info"""
    print(*args,file=out)


# MAIN program
if __name__ == "__main__":
    # Command line options
    p = argparse.ArgumentParser("Author identification")
    p.add_argument("DIR",default=None,
            action="store", help="Directory with examples")
    p.add_argument("Answers",default=None, nargs='?',
            action="store", help="File with the key answers")
    p.add_argument('--version', action='version', version='%(prog)s 0.2')
    p.add_argument("-o", "--output",default=None,
            action="store", dest="output",
            help="Output [STDOUT]")
    p.add_argument("-m", "--mode",default='devel',
            action="store", dest="mode",
            help="test|train|devel [test]")
    p.add_argument("-r","--rep",default=['bow'],
            action="append", dest="reps",
            help="adds representation to process")
    p.add_argument("--cutoff",default=2,type=int,
            action="store", dest="cutoff",
            help="Minimum frequency [5]")
    p.add_argument("--iters",default=35,type=int,
            action="store", dest="iters",
            help="Total iterations [35]")
    p.add_argument("--lang",default=None,
            action="store", dest="language",
            help="Language to process")
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
            help="Sampling percentage [.60]")
    p.add_argument("--model",default=".",
            action="store", dest="model",
            help="Model to save training or to test with [None]")
    p.add_argument("--random",default=True,
            action="store_false", dest="random",
            help="Use random seed [True]")
    p.add_argument("--dumpfiles",default=False,
            action="store_true", dest="dump",
            help="Record dump files [False]")
    p.add_argument("--stopwords", default=None,
            action="store", dest="stopwords",
            help="List of stop words [None, uses default]")
    p.add_argument("--answers", default="answers.txt",
            action="store", dest="answers",
            help="Answers file [answers.txt]")
    p.add_argument("--processors",default=1,type=int,
            action="store", dest="nprocessors",
            help="Number of processors [1]")
    p.add_argument("-v", "--verbose",
            action="store_true", dest="verbose",
            help="Verbose mode [Off]")
    opts = p.parse_args()

    # Managing configuration ----------------------------------------------
    if not opts.random:
        random.seed(9111978)
    opts.reps=list(set(opts.reps))
    opts.genre='all'

    # prepara función de verbose
    if opts.verbose:
        def verbose(*args,**kargs):
            print(*args,**kargs)
    else:   
        verbose = lambda *a: None 


    # Defines output
    if opts.output:
        try:
            out = open(opts.output)
        except:
            p.error('Output parameter could not been open: {0}'\
                    .format(opts.output))

    # Check the correct mode
    if not opts.mode in ["train","test","devel"]:
        p.error('Mode argument not valid: devel, train  test')
    verbose("Running in mode:",opts.mode)

    # Parameters -----------------------------------------------------------
    # Patterns for files
    known_pattern=r'known.*\.txt$'
    unknown_pattern=r'unknown*.txt$'

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
    if not opts.language:
        with open("{0}/{1}".format(opts.DIR,'contents.json')) as data_file:    
            jinfo = json.load(data_file)
        if jinfo['language'].startswith('Dutch'):
            opts.language="nl"
        if jinfo['language'].startswith('Spanish'):
            opts.language="es"
        if jinfo['language'].startswith('English'):
            opts.language="en"
        if jinfo['language'].startswith('Greek'):
            opts.language="gr"

    # Loading stopwords if exits
    stopwordspat="data/stopwords_{0}.txt"
    stopwords=[]
    if not opts.stopwords:
        fstopwords=stopwordspat.format(config.codes[opts.language]['stopwords'])
    else:
        fstopwords=opts.stopwords
    if os.path.exists(fstopwords):
        verbose('Loading stopwords: ',fstopwords)
        stopwords=docread.readstopwords(fstopwords)
    else:
        info('Stopwords file not found assuming emtpy',opts.stopwords)

    # Loading main files -------------------------------------------------
    # load problems
    verbose('Loading files')
    problems=docread.problems(
             docread.dirproblems(opts.DIR,known_pattern,unknown_pattern,_ignore,
                                 code=config.codes[opts.language][opts.genre]))
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

    # Loading answers file only for DEVELOPMENT OR TRAINNING MODE
    if opts.mode.startswith("train") or opts.mode.startswith('devel'):
        if opts.Answers:
            answers_file=opts.Answers
        else:
            answers_file="{0}/{1}".format(opts.DIR,opts.answers)
        verbose('Loading answer file: {0}'.format(answers_file))
        answers = docread.loadanswers(answers_file,_ignore,
                code=config.codes[opts.language][opts.genre])

        # Checking for consistency
        if not len(problems) == len(answers):
            p.error("Not match for number of problems({0}) and \
                    answers({1})".format(len(problems),len(answers)))

    # Development model 
    if opts.mode.startswith("devel"):
        verbose('Starting the process')
        hbc.process_corpus(problems,impostors,opts,"devel",sw=stopwords,verbose=verbose)
      
    # TRAINING - Save examples
    elif opts.mode.startswith("train"):
        verbose("Nothing to do ",opts.model)

    elif opts.mode.startswith("test"):
        verbose("Labeling corpus ",opts.model)
        hbc.process_corpus(problems,impostors,opts,"test",sw=stopwords,verbose=verbose)
