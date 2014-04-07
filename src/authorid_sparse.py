#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Author ID main using a sparse representation
# ----------------------------------------------------------------------
# Ivan V. Meza
# 2014/IIMAS, México
# ----------------------------------------------------------------------
# authorid_bayes.py is free software: you can redistribute it and/or modify
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
import itertools
import random
from collections import Counter
from cvxopt import matrix

# Local imports
import docread

def verbose(*args):
    """ Function to print verbose"""
    if opts.verbose:
        print >> out, "".join(args)

def info(*args):
    """ Function to print info"""
    print >> out, "".join(args)

def muestreo(counter,percentage=.80):
   list_counter=list(counter.elements())
   random.shuffle(list_counter)
   
   size=len(list_counter)
   final_list=list_counter[0:int(size*percentage)]  
  
   final_count=Counter(final_list)  
   return final_count

def get_master_impostors(id,n,problems,sw=[]):
    master_impostors=[]
    pat=id[:2]
    ids_candidates=[]
    for id_,(ks,uks) in problems:
        if id_.startswith(pat) and id != id_:
            ids_candidates.append(id_)
    random.shuffle(ids_candidates)
    
    for id_,(ks,uks) in problems:
        if id_ in ids_candidates[:n]:
            master_candidate=Counter()
            for doc in ks:
                ngram=docread.ngram(doc[1])[0]
                master_candidate.update(ngram)
            master_impostors.append(master_candidate)
    return master_impostors
 

def proyect_into_vectors(exmamples,unknown, nmost=200):
    full=Counter()
    for example in examples:
        full.update(example)
    full.update(unknown)

    idx=[p[0] for p in full.most_common()[:100]]
    vectors=[]
    for example in examples:
        arr=[1.0*example[k] for k in idx]
        vectors.append(arr)
    return vectors,[1.0*unknown[k] for k in idx]


codes=docread.codes

# MAIN program
# if __name__ == "__main__

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
    p.add_argument("--off",default=[],
            action="append", dest="off",
            help="distances or representations to turn off")
    p.add_argument("--model",default=".",
            action="store", dest="model",
            help="Model to save training or to test with [None]")
    p.add_argument("--cvs",default=False,
            action="store_true", dest="csv",
            help="Save matrices into a .csv file [False]")
    p.add_argument("--method",default="lp",
            action="store", dest="method",
            help="lp|avp|svm|ann [lp]")
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

    if opts.csv:
        import csv
        file_A=open("A.csv","w")
        csv_A=csv.writer(file_A,delimiter=',',quotechar=",")
        file_b=open("b.csv","w")
        csv_b=csv.writer(file_b,delimiter=',',quotechar=",")


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
	#Iterating over problems
        for id,(ks,uks) in problems:
            master_author=Counter()
            master_unknown=Counter()
     
            for filename,doc in ks:
                ngram=docread.ngram(doc)[0]
                master_author.update(ngram)

            for filename,doc in uks:
                ngram=docread.ngram(doc)[0]
                master_unknown.update(ngram)

            #Extracting Examples
            examples= []
            for i in range(4):
                examples.append(muestreo(master_author))

            # Adding imposters
            master_impostors=get_master_impostors(id,10,problems)
            for master_impostor in master_impostors:
                 for i in range(4):
                    examples.append(muestreo(master_impostor))

            # Sparce algorithm
            # Proyecting examples into a vector
            example_vectors,unknown=proyect_into_vectors(examples,master_unknown)
            # Creating matrix A
            # First samples represent to author, rest impostors
            A=np.array(example_vectors)
            tolerance=0.01
            # Normalizing the data
            A=preprocessing.normalize(example_vectors,axis=0)
            A=A.T
            A=matrix(A)
            y=matrix(unknown)
            # Solve l1
            from l1 import l1
            from cvxopt import solvers
            solvers.options['show_progress'] = False
            try:
                x_0 = l1(A,y)
                # Calculating residuals
                residuals=[]
                for i in range(len(examples)/4):
                    d_i= [0.0 for x in x_0[:i*4]]+\
                         [x for x in x_0[i*4:(i+1)*4]]+\
                         [0.0 for x in x_0[(i+1)*4:]]

                    d_i=matrix(d_i)
                    r_is=y-A*d_i
                    r_is_2=sum(r_is**2)
                    r_i=np.sqrt(r_is_2)
                    residuals.append(r_i)
                identity=np.argmin(residuals)
                if identity==0:
                    print id, "0.7"
                else:
                    print id, "0.2"
            except ValueError:
                print id, "0.5"
            if opts.csv:
                m,n=A.size
                vals=[]
                for val in A:
                    vals.append(val)
                csv_A.writerow([id,11,m,n]+vals)
                m,n=y.size
                csv_b.writerow([id,11,m,n]+[x for x in y])

	   

    # TRAINING - Save examples
    elif opts.mode.startswith("train"):
        import pickle
        
        stream_model = pickle.dumps(problems)
        verbose("Saving model into ",opts.model)
        with open(opts.model,"w") as modelf:
            modelf.write(stream_model)

 
    elif opts.mode.startswith("test"):
        pass	
