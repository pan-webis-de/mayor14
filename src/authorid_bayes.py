#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Author ID main 
# ----------------------------------------------------------------------
# Paola Ledesma 
# 2013/ENAH
# Gibran Fuentes
# 2013/IIMAS/UNAM
# Gabriela Jasso
# 2013/FI/UNAM
# Ángel Toledo
# 2013/FC/UNAM
# Ivan Vladimir Meza-Ruiz/ ivanvladimir at turing.iimas.unam.mx
# 2013/IIMAS/UNAM
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

def posneg(val):
    """ Given the value it decides if it is the author (Y) or not (N)"""
    if val<0.5:
        return "Y"
    else:
        return "N"



def train(method, X_train,Y_train):
    model=None
    if method.startswith('svm'):
        model   = ML.svmtrain(X_train,Y_train)
    elif method.startswith('avp'):
        model   = ML.avptrain(X_train,Y_train,opts.iters)
    elif method.startswith('ann'):
        model   = ML.anntrain(X_train,Y_train)#,opts.iters)
    elif method.startswith('lp'):
        try:
            model    = ML.lptrain(X_train,Y_train)
        except TypeError:
            model = None
    return model

def predict(method,model, X_test, Y_test):
    # predict
    if method.startswith('svm'):
        preds = ML.svmtest(model,X_test,Y_test)
    elif method.startswith('avp'):
        preds = ML.avptest(model,model)
    elif method.startswith('ann'):
        preds = ML.anntest(X_test,model)
    elif method.startswith('lp'):
        preds = ML.lptest(X_test,model)
    else:
        preds = ML.lptest(X_test,[(1.0/15) 
                    for x in X_test[0]])


   
    return preds

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

def muestreo(counter):

   list_counter=list(counter.elements())
   random.shuffle(list_counter)
   
   size=len(list_counter)
   final_list=list_counter[0:int(size*60/100)]  
  
   final_count=Counter(final_list)  
   return final_count

   

# MAIN program
if __name__ == "__main__":

    version="%prog 0.1"

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
    p.add_argument("--norm",default=True,
            action="store_true", dest="norm",
            help="Normalize vector space [True]")
    p.add_argument("--off",default=[],
            action="append", dest="off",
            help="distances or representations to turn off")
    p.add_argument("-i", "--iters",default=100,type=int,
            action="store", dest="iters",
            help="Number of iterations for avg [10]")
    p.add_argument( "--model",default="pan14.model",
            action="store", dest="model",
            help="Model to save training or to test with [None]")
    p.add_argument("--method",default="lp",
            action="store", dest="method",
            help="lp|avp|svm|ann [lp]")
    p.add_argument("--show-figures", default=False,
            action="store_true", dest="showf",
            help="Shows figures [None]")
    p.add_argument("--figures", default=None,
            action="store", dest="figures",
            help="Save figures in directory [None]")
    p.add_argument("--stopwords", default="data/stopwords.txt",
            action="store", dest="stopwords",
            help="List of stop words [data/stopwords.txt]")
    p.add_argument("--answers", default="Answers.txt",
            action="store", dest="answers",
            help="Answers file [Answers.txt]")
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
        docread.dirproblems(dirname,known_pattern,unknown_pattern,_ignore))

    
    # Loading answers file only for DEVELOPMENT OR TRAINNING MODE
    if opts.mode.startswith("train"):
        if opts.Answers:
            answers_file=opts.Answers
        else:
            answers_file="{0}/{1}".format(args[0],opts.answers)
        verbose('Loading answer file: {0}'.format(answers_file))
        answers = docread.loadanswers(answers_file,_ignore)

        # Checking for consistency
        if not len(problems) == len(answers):
            p.error("Not match for number of problems({0}) and \
            answers({1})".format(len(problems),len(answers)))


    samples=[]
    classes=[]
    imposter_EN=[0,0,0,0,0,0,0,0,0,0]
    imposter_GR=[0,0,0,0,0,0,0,0,0,0]
    imposter_SP=[0,0,0,0,0,0,0,0,0,0]
    L = [list(range(60)) for i in range(60)]#initilizing n-gram counters
    # Create the representations for known and unknown documents
   # print "making imposters"
    for id,(ks,uks) in problems:
	
        verbose('Reading from : {0}'.format(id))
           
        if len(uks) > 1:
            p.error("More than one unknown file for {0}".format(id))
       
        # Builds uknnown representation of document
        docreps_=[]
        for rep,f in docread.representations:
            if rep in opts.off:
                continue
            docreps_.append((rep,f(uks[0][1],stopwords)))

	 # Builds known representations of documents 
        docs = []        
        for k in ks:
	   
            docreps=[]
            for rep,f in docread.representations:
                if rep in opts.off:
                    continue
                docreps.append((rep,f(k[1],stopwords)))
            docs.append(docreps)
            
	    	
        samples_=[]
        classes_=[]
	

	
	if opts.mode.startswith("test"):
	  # print "Impostors"
	   if id.find("EN")>=0:
	      for i in range(len(ks)):
		(aux,x,boolean)=impostor_list(docs,imposter_EN,i)
		if boolean:
		   L[0+(i*2)-x][0]=id
		   L[0+(i*2)-x][1]=aux
	   if id.find("GR")>=0:
	      for i in range(len(ks)):
		(aux,x,boolean)=impostor_list(docs,imposter_GR,i)
		if boolean:
		   L[10+(i*2)-x][0]=id
		   L[10+(i*2)-x][1]=aux
	   if id.find("SP")>=0:
	      for i in range(len(ks)):
		(aux,x,boolean)=impostor_list(docs,imposter_SP,i)
		if boolean:
		   L[20+(i*2)-x][0]=id
		   L[20+(i*2)-x][1]=aux
           
           

    if opts.mode.startswith("test"):
	 #print "Calculating answers"
	 for id,(ks,uks) in problems:
		
		verbose('Reading from : {0}'.format(id))
		
		if len(uks) > 1:
		    p.error("More than one unknown file for {0}".format(id))
	       
		# Builds uknnown representation of document
		docreps_=[]
		for rep,f in docread.representations:
		    if rep in opts.off:
		        continue
		    docreps_.append((rep,f(uks[0][1],stopwords)))


		# Builds known representations of documents 
		docs = []
		
		for k in ks:
		   
		    docreps=[]
		    for rep,f in docread.representations:
		        if rep in opts.off:
		            continue
		        docreps.append((rep,f(k[1],stopwords)))
		    docs.append(docreps)
		 
		count_final1=Counter()
	        count_final2=Counter()
		   
		count_aux=ngrams_test(docs,len(ks))
		counter_final1=muestreo(count_aux)
		counter_final2=muestreo(count_aux)
		knows_intersection = (counter_final1 & counter_final2)
	

		#search imposter
		   
		if id.find("EN")>=0:
			i=0
		if id.find("GR")>=0:
			i=10
		if id.find("SP")>=0:
			i=20
		j=len(ks)
		k=0
		if L[i+j+k][0]==id:#imposter
			k=1
                
		
		counter_imposter1=muestreo(L[i+j+k][1])
		counter_imposter2=muestreo(L[i+j+k][1])
		intersection_imposter = (counter_imposter1 & counter_imposter2)
		
		counter_uks=Counter()
		for j in range(len(docread.representations)):
		   counter_uks+= docreps_[j][1][0]
		set_uks = set(counter_uks)#elementos sin repeticion

		#Bayes
		bayes_uks_imposter=0.5
		bayes_uks_knows=0.5
		for i in range(len(set_uks)):
			
  			if (knows_intersection[list(set_uks)[i]]!= 0):
			   bayes_uks_knows+=math.log(knows_intersection[list(set_uks)[i]],10)	 
			if (intersection_imposter[list(set_uks)[i]]!= 0):	
			   bayes_uks_imposter+=math.log(intersection_imposter[list(set_uks)[i]],10)
		#comparing 
		if bayes_uks_knows > bayes_uks_imposter:
		      answer = "Y"
		else: 
		      answer  = "N"
		probability=(bayes_uks_knows)/( bayes_uks_knows+ bayes_uks_imposter)
		wr=id+" "+str(probability)
		print wr

		#print ("answer ",answer,"probability ",(bayes_uks_knows)/( bayes_uks_knows+ bayes_uks_imposter))

	
     
