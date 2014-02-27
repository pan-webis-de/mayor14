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
    if opts.mode.startswith("train") or opts.mode.startswith("devel"):
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
    # Create the representations for known and unknown documents
    for id,(ks,uks) in problems:
        verbose('Reading from : {0}'.format(id))
            # Load unknown 
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

        # Compares each known docuemnt to unknown document
        for idoc,docreps in enumerate(docs):
            verbose('Comparing with: {0}'.format(ks[idoc][0]))
            feats=[]
	    commons=Counter()
            for doc,doc_ in zip(docreps,docreps_): 
                verbose("-- {0} --".format(doc_[0]))
                for n,f in distance.distances:
                    if n in opts.off:
                        continue
                    A=doc_[1][0]
                    B=doc[1][0]
                    d=f(A,B)
                    verbose("{0} distance".format(n).ljust(30),
                            "{0:0.4f}".format(d))
                    feats.append(d)

		    #print d
		   
                commons.update(doc[1][1])
            #_tmp=[feats]	  
            # Figures out the language by common words
            _tmp=[0,0,0]
            if commons['the']>=1:
                _tmp[0]=feats
                _tmp[1]=[0.0 for x in feats]
                _tmp[2]=[0.0 for x in feats]
            elif commons['el']>=1:
                _tmp[0]=[0.0 for x in feats]
                _tmp[1]=feats
                _tmp[2]=[0.0 for x in feats]
            else:
                _tmp[0]=[0.0 for x in feats]
                _tmp[1]=[0.0 for x in feats]
                _tmp[2]=feats
	    

	    feats=list(itertools.chain(*_tmp))         
            samples_.append(feats)
            # Creating answers only if TRAINING or DEVELPMENT
            if opts.mode.startswith("train") or opts.mode.startswith("devel"):
                info('Answer to unknown: {0}'.format(answers[id]))
                if answers[id].startswith('Y'):
                    ANS=0 # Close in distance
                else:
                    ANS=1 # Far in distance
                classes_.append(ANS)

        # Vectors for each document-distance-representation
        samples.append(samples_)
        classes.append(classes_)

    
    # DEVELOPMENT OR TRAINNING MODE
    if opts.mode.startswith("train") or opts.mode.startswith("devel"):
        tp=0.0
        fp=0.0
        fn=0.0
        # For trainning 
        if opts.mode.startswith("devel"):
            info('Leave one out setting for development')
            Total =0.0
            N_Acc =0
            Total_=0.0
            N_Acc_=0
            # leave-one-out crossvalidation
            sin_contestar=0
	    for i in range(len(samples)):

                # Creates train corpus for cross validation
                info('Model for ',str(i))
                X_train = samples[:i]+samples[i+1:]
                X_train = list(itertools.chain(*X_train))
                Y_train = classes[:i]+classes[i+1:]
                Y_train = list(itertools.chain(*Y_train))
                # Creates test corpus for cross validation (1 sample)
                Y_test  = classes[i]
                X_test  = samples[i]

                # Train and test
                model=train(opts.method,X_train,Y_train)
                preds=predict(opts.method,model,X_test,Y_test)
                res=ML.voted(preds)
                prob= ML.proba(preds)

                # Calculate metrics
                if res==answers[problems[i][0]]:
                    pref=""
                    N_Acc+=1
                    tp+=1
                else:
                    if res=='':
                        fn+=1
                    else:
                        fp+=1
                        fn+=1
                    pref="**"
                Total+=1

                for x,x_ in zip(preds,Y_test):
                    if x[0]==x_:
                        N_Acc_+=1
                    Total_+=1

                # Print information for sample
                verbose(pref,"Model       ",problems[i][0])
                verbose(pref,"Predictions "," ".join(["{0}/{1:0.2}".format(posneg(x),y)
                                                for x,y in preds]))
                verbose(pref,"GSs         "," ".join([posneg(x) for x in Y_test]))
                verbose(pref,"Prediction  ",res)
                verbose(pref,"GS          ",answers[problems[i][0]])
                verbose(pref,"probability  ",str(prob))
                info(">>>>",problems[i][0]," {0} ".format(res))
		
		if prob =="0.5":
		  sin_contestar=sin_contestar+1

	    # Print metric for the whole samples

	    c=100.0*(1/float(Total))*(tp+(sin_contestar*tp/float(Total)))
	    info('Accuracy over all decisions : {0:3.3f}%'.format(100.0*N_Acc_/Total_))
            info('Accuracy over problems : {0:3.3f}%'.format(100.0*N_Acc/Total))
            pres=100.0*tp/(tp+fp)
            recall=100.0*tp/(tp+fn)
            info('Precision : {0:3.3f}%'.format(pres))
            info('c@1       : {0:3.3f}%'.format(c))
	    info('Recall    : {0:3.3f}%'.format(recall))
            info('F1-score  : {0:3.3f}%'.format(2*pres*recall/(pres+recall)))
        # Trains and saves the model
        elif opts.mode.startswith("train"):
            import pickle
            
            # Prepares data for training
            X_train = samples
            X_train = list(itertools.chain(*X_train))
            Y_train = classes
            Y_train = list(itertools.chain(*Y_train))

            model =train(opts.method,X_train,Y_train)
            stream_model = pickle.dumps(model)
            verbose("Saving model into ",opts.model)
            with open(opts.model,"w") as modelf:
                modelf.write(stream_model)
    # TEST model
    elif opts.mode.startswith("test"):
      
        # Load model
        import pickle
        with open(opts.model,"r") as model:
            s=model.read()
        # Labels each sample
        for i in range(len(samples)):
            X_test  = samples[i]

            model = pickle.loads(s)
            preds = predict(opts.method,model,X_test,[])
            res=ML.voted(preds)
            prob= ML.proba(preds)
 	    #info('Model for ',str(i))
            
            info(problems[i][0]," {0} ".format(prob))
            verbose("Predictions "," ".join(["{0}/{1:0.6}".format(posneg(x),y)
                                                for x,y in preds]))
	    verbose("probability ",str(prob))
       
    else:
        info("Error with mode",opts.mode)


 


