#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Author ID main 
# ----------------------------------------------------------------------
# Cristhian Mayor
# 2014/INSA Lyon
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
import math
import itertools
import random
from collections import Counter
from collections import defaultdict

# Local imports
import docread
import distance
import ML

def verbose(*args):
    """ Function to print verbose"""
    if opts.verbose:
        print >> out, "".join(args)

def info(*args):
    """ Function to print info"""
    print >> out, "".join(args)

def impostor_list(docs,impostor_l,i):
      count_aux=Counter()
      if (impostor_l[i] < 2):
	impostor_l[i]+=1
	for h in range(0,i+1):
	   for j in range(len(docread.representations)):
	      count_aux+=docs[h][j][1][0] 
	boolean =1
      else :
	boolean =0
      return count_aux,impostor_l[i],boolean

def ngrams_test(docs,i):
      count_aux=Counter()
      for h in range(0,i):
	for j in range(len(docread.representations)):
	   count_aux+=docs[h][j][1][0] 
	
      return count_aux

def muestreo(counter,percentage=.80):
   list_counter=list(counter.elements())
   random.shuffle(list_counter)
   
   size=len(list_counter)
   final_list=list_counter[0:int(size*percentage)]  
  
   final_count=Counter(final_list)  
   return final_count


def get_impostor(id,n, problems,sw=[]):
    candidates=[]
    pat=id[:2]
    docs=Counter()
    ids_candidates=[]
    for id_,(ks,uks) in problems:
        if id_.startswith(pat) and id != id_:
            ids_candidates.append(id_)
    random.shuffle(ids_candidates)
    
    for id_,(ks,uks) in problems:
        if id_ in ids_candidates[:10]:
           for doc in ks:
                candidates.append(doc[1])
 
    candiates=list(itertools.chain(*candidates))
    random.shuffle(candiates)
    for can in candidates[:n]:
        docs.update(Counter(dict(docread.ngram(can,sw=sw)[1])))
    return docs
        
    
   
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
    p.add_argument( "--model",default=".",
            action="store", dest="model",
            help="Model to save training or to test with [None]")
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
    if opts.mode.startswith("train"):
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

    if opts.mode.startswith("test"):
	 #print "Calculating answers"
	 for id,(ks,uks) in problems:
		
		verbose('Reading from : {0}'.format(id))
		
		if len(uks) > 1:
		    p.error("More than one unknown file for {0}".format(id))
	       

                count_aux=Counter()		
                for filename,doc in ks:
                    
                    ngram=Counter(dict(docread.ngram(doc,sw=stopwords)[1]))
                    count_aux.update(ngram)
		counter_final1=muestreo(count_aux)
		counter_final2=muestreo(count_aux)
		knows_intersection = (counter_final1 & counter_final2)
	
                
                impostor=get_impostor(id,len(ks),problems,sw=stopwords)
		counter_imposter1=muestreo(impostor)
		counter_imposter2=muestreo(impostor)
		intersection_imposter = (counter_imposter1 & counter_imposter2)
	
		counter_uks=Counter(dict(docread.ngram(uks[0][1],sw=stopwords)[1]))
		set_uks = set(counter_uks.keys()) #elementos sin repeticion

		#Bayes
		bayes_uks_imposter=0.5
		bayes_uks_knows=0.5
		for word in set_uks:
  			if (knows_intersection[word]!= 0):
			   bayes_uks_knows+=math.log(min(counter_uks[word],knows_intersection[word]),10)	 
			if (intersection_imposter[word]!= 0):	
			   bayes_uks_imposter+=math.log(min(counter_uks[word],intersection_imposter[word]),10)
		#comparing 
		if bayes_uks_knows > bayes_uks_imposter:
		      answer = "Y"
		else: 
		      answer  = "N"
		probability=(bayes_uks_knows)/( bayes_uks_knows+ bayes_uks_imposter)
		wr=id+" "+str(probability)
		print wr

		#print ("answer ",answer,"probability ",(bayes_uks_knows)/( bayes_uks_knows+ bayes_uks_imposter))

	
     
