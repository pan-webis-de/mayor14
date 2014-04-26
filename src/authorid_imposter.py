#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Author ID main using imposters
# ----------------------------------------------------------------------
# Josue Gutierrez
# 2014/Showroom, México
# Ivan V. Meza
# 2014/IIMAS, México
# ----------------------------------------------------------------------
# authorid_imposter.py is free software: you can redistribute it and/or modify
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
import os,re, sys, glob, codecs, requests, justext , shutil, time
import numpy as np
from BeautifulSoup import BeautifulSoup

import argparse
import sys
import os
import os.path
import numpy as np
import random
import itertools
from collections import Counter


# Local imports
import docread
import distance

def verbose(*args):
    """ Function to print verbose"""
    if opts.verbose:
        print >> out, "".join(args)

def info(*args):
    """ Function to print info"""
    print >> out, "".join(args)

def muestreo(counter,reps,percentage=.80):
    final_count=Counter()
    for rep in reps:
        
        if len(counter[rep].keys()) < 120:
            percentage_=1.0
        else:
            percentage_=percentage

        list_counter=list(counter[rep].elements())
        random.shuffle(list_counter)
       
        size=len(list_counter)
        final_list=list_counter[0:int(size*percentage_)]  
      
        final_count.update(final_list)  
    return final_count

def get_master_impostors(id,n,problems,sw=[],mode="test"):
    if mode.startswith("test"):
        id=id+"___"
    master_impostors=[]
    lens=[]
    pat=id[:2]
    ids_candidates=[]
    for id_,(ks,uks) in problems:
        if id_.startswith(pat) and id != id_:
            ids_candidates.append(id_)
    random.shuffle(ids_candidates)
    
    for id_,(ks,uks) in problems:
        if id_ in ids_candidates[:n]:
            master_candidate={}
            for doc in ks:
                for repname in opts.reps:
                    try:
                        exec("f=docread.{0}".format(repname))
                        rep=f(doc[1])[0]
                    except:
                        rep=Counter()
                    try:
                        master_candidate[repname].update(rep)
                    except KeyError:
                        master_candidate[repname]=Counter(rep)

            master_impostors.append(master_candidate)
    return master_impostors
 

def proyect_into_vectors(examples,full_voca,unknown,reps,lens,nmost=120):
    vectors=[[] for e in examples]
    uvec=[]
    for rep in reps:
        full=Counter()
        for example in examples:
            full.update(example[rep])
        full.update(unknown[rep])
        idx=[p[0] for p in full.most_common()[:nmost]]
        for i,example in enumerate(examples):
            arr=[1.0*example[rep][k] for k in idx]
            vectors[i].append(arr)
        uvec.append([1.0*unknown[rep][k] for k in idx])
    return [list(itertools.chain(*vec)) for vec in vectors], list(itertools.chain(*uvec))

codes=docread.codes


def process_corpus(problems,impostor_problems,opts,mode):
	#Iterating over problems
        for id,(ks,uks) in problems:
            master_author={}
            master_unknown={}
            full_voca={}
     
            for filename,doc in ks:
                for repname in opts.reps:
                    try:
                        exec("f=docread.{0}".format(repname))
                        rep=f(doc)[0]
                    except:
                        rep=Counter()
                    try:
                        master_author[repname].update(rep)
                    except KeyError:
                        master_author[repname]=Counter(rep)
                    try:
                        full_voca[repname].update(rep)
                    except KeyError:
                        full_voca[repname]=Counter(rep)

            for filename,doc in uks:
                 for repname in opts.reps:
                    try:
                        exec("f=docread.{0}".format(repname))
                        rep=f(doc)[0]
                    except:
                        rep=Counter()
                    try:
                        master_unknown[repname].update(rep)
                    except KeyError:
                        master_unknown[repname]=Counter(rep)
                    try:
                        full_voca[repname].update(rep)
                    except KeyError:
                        full_voca[repname]=Counter(rep)

            results=[]
            iters=opts.iters
            score=0.0
            for iter in range(iters):
                known_sample=muestreo(master_author,opts.reps,percentage=opts.percentage)
                unknown_sample=muestreo(master_unknown,opts.reps,percentage=opts.percentage)

                # Adding imposters
                master_impostors=get_master_impostors(id,opts.imposters,impostor_problems,mode)

                for master_impostor in master_impostors :
                    imposter_sample=muestreo(master_impostor,opts.reps,percentage=opts.percentage)


                    dk_di = distance.jacard2(known_sample, imposter_sample)
                    dk_du = distance.jacard2(known_sample, unknown_sample)
                    du_di = distance.jacard2(unknown_sample, imposter_sample)
                    du_dk = distance.jacard2(unknown_sample, known_sample)

                    if dk_du * du_dk > dk_di * du_di :
                        score += 1/ float( (opts.iters) * len(master_impostors) )

            print id, 1.0-score




# MAIN program
if __name__ == "__main__":
    # Command line options
    p = argparse.ArgumentParser("Author identification")
    p.add_argument("DIR",default=None,
            action="store", help="Directory with examples")
    p.add_argument("Answers",default=None,
            action="store", help="File with the key answers")
    p.add_argument('--version', action='version', version='%(prog)s 0.2')
    p.add_argument("-o", "--output",default=None,
            action="store", dest="output",
            help="Output [STDOUT]")
    p.add_argument("-m", "--mode",default='test',
            action="store", dest="mode",
            help="test|train|devel [test]")
    p.add_argument("--language",default='all',
            action="store", dest="language",
            help="Language to process [all]")
    p.add_argument("--genre",default='all',
            action="store", dest="genre",
            help="Genre to process [all]")
    p.add_argument("-r","--rep",default=[],
            action="append", dest="reps",
            help="adds representation to process")
    p.add_argument("--threshold",default=0.5,type=float,
            action="store", dest="threshold",
            help="Threshold to consider id an author [0.5]")
    p.add_argument("--iters",default=10,type=int,
            action="store", dest="iters",
            help="Total iterations [10]")
    p.add_argument("--imposters",default=100,type=int,
            action="store", dest="imposters",
            help="Total of imposters [100]")
    p.add_argument("--percentage",default=.95,type=float,
            action="store", dest="percentage",
            help="Sampling percentage [.95]")
    p.add_argument("--model",default=".",
            action="store", dest="model",
            help="Model to save training or to test with [None]")
    p.add_argument("--stopwords", default="data/stopwords.txt",
            action="store", dest="stopwords",
            help="List of stop words [data/stopwords.txt]")
    p.add_argument("--answers", default="answers.txt",
            action="store", dest="answers",
            help="Answers file [answers.txt]")
    p.add_argument("-v", "--verbose",
            action="store_true", dest="verbose",
            help="Verbose mode [Off]")
    opts = p.parse_args()


    # Managing configurations  --------------------------------------------
    # Check the correct mode
    if not opts.mode in ["train","test","devel"]:
        p.error('Mode argument not valid: devel, train  test')

    # Parameters
    # Patterns for files
    known_pattern=r'known.*\.txt'
    unknown_pattern=r'unknown*.txt'

    dirname = opts.DIR

    # Defines output
    out = sys.stdout
    if opts.output:
        try:
            out = open(opts.output)
        except:
            p.error('Output parameter could not been open: {0}'\
                    .format(opts.output))
    verbose("Running in mode:",opts.mode)

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
        
    # Loading answers file only for DEVELOPMENT OR TRAINNING MODE
    if opts.mode.startswith("train") or opts.mode.startswith('devel'):
        if opts.Answers:
            answers_file=opts.Answers
        else:
            answers_file="{0}/{1}".format(dirname,opts.answers)
        verbose('Loading answer file: {0}'.format(answers_file))
        answers = docread.loadanswers(answers_file,_ignore,
                code=codes[opts.language][opts.genre])

        # Checking for consistency
        if not len(problems) == len(answers):
            p.error("Not match for number of problems({0}) and \
                    answers({1})".format(len(problems),len(answers)))

    # Development model 
    if opts.mode.startswith("devel"):
        process_corpus(problems,problems,opts,"devel")
 

