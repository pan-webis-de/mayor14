#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Author ID main 
# ----------------------------------------------------------------------
# Ivan Vladimir Meza-Ruiz/ ivanvladimir at turing.iimas.unam.mx
# 2012/IIMAS/UNAM
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
import optparse
import sys
import os
import os.path
import itertools

# Local imports
import docread
import distance
import ML

def verbose(*args):
    if opts.verbose:
        print >> out, "".join(args)

def info(*args):
    print >> out, "".join(args)

def posneg(val):
    if val:
        return "Y"
    else:
        return "N"

# MAIN
if __name__ == "__main__":
    usage="""%prog [options] dir [anwers]

        Runs user identification 

        dir   : Directory with author examples
        answer: File with answers for trainning
"""

    version="%prog 0.1"

    # Command line options
    p = optparse.OptionParser(usage=usage,version=version)
    p.add_option("-o", "--output",default=None,
            action="store", dest="output",
            help="Output [STDOUT]")
    p.add_option("-m", "--mode",default='test',
            action="store", dest="mode",
            help="test|train [test]")
    p.add_option("-i", "--iters",default=10,type="int",
            action="store", dest="iters",
            help="Number of iterations for avg [10]")
    p.add_option("-w", "--weights",default=None,
            action="store", dest="weights",
            help="weights file [None]")
    p.add_option("", "--method",default="avp",
            action="store", dest="method",
            help="avp|svm [avp]")
    p.add_option("", "--known_pattern",default=r'known.*\.txt',
            action="store", dest="known",
            help="pattern for known files [known*]")
    p.add_option("", "--unknown_pattern",default=r'unknown*.txt',
            action="store", dest="unknown",
            help="pattern for unknown file [unknown*]")
    p.add_option("", "--figures", default=None,
            action="store", dest="figures",
            help="Save figures in directory [None]")
    p.add_option("-v", "--verbose",
            action="store_true", dest="verbose",
            help="Verbose mode [Off]")
    opts, args = p.parse_args()

    # Arguments 
    if not len(args) > 0:
        p.error('Wrong number of arguments')

    if not opts.mode in ["train","test"]:
        p.error('Mode argument not valid: train or test')

    if opts.figures:
        import numpy as np
        import matplotlib
        import matplotlib.pyplot as plt



    dirname = args[0]

    # Parameters
    out = sys.stdout
    if opts.output:
        try:
            out = open(opts.output)
        except:
            p.error('Output parameter could not been open: {0}'\
                    .format(opts.output))

    # Loading ingnore if exists
    _ignore=[]
    if os.path.exists('.ignore'):
        verbose('Loading files to ignore frm: .ignore')
        with open('.ignore') as file:
            _ignore=file.read().readlines()

        
    # load problems or problem
    problems=docread.dirproblems(dirname,opts.known,opts.unknown,_ignore)

    # TRAINNING MODE
    if opts.mode.startswith("train"):
      
        # Loading answers file
        if not len(args)==2:
            p.error("Answers needed for train mode")
        verbose('Loading answer file: {0}'.format(args[1]))
        answers = docread.loadanswers(args[1])

        # Checking for consistency
        if not len(problems) == len(answers):
            p.error("Not match for number of problems({0}) and \
            answers({1})".format(len(problems),len(answers)))


        samples=[]
        classes=[]
        # Transforms documents into samples 
        for id,(ks,uks) in problems:
            info('Reading from : {0}'.format(id))
            info('Answer to unknown: {0}'.format(answers[id]))
            if answers[id].startswith('Y'):
                ANS=0.0
            else:
                ANS=1.1

            # Load unknown 
            if len(uks) > 1:
                p.error("More than one unknown file for {0}".format(id))
           
            # Builds uknnown representation of document
            docreps_=[]
            for rep,f in docread.representations:
                docreps_.append((rep,f(uks[0])))

            # Load knowns 
            docs = []
            for k in ks:
                docreps=[]
                for rep,f in docread.representations:
                    docreps.append((k,f(k)))
                docs.append(docreps)
                
            verbose('Loading files')
            samples_=[]
            classes_=[]
            for docreps in docs:
                verbose('Comparing with: {0}'.format(k))
                feats=[]
                for doc,doc_ in zip(docreps,docreps_): 
                    verbose("-- {0} --".format(doc_[0]))
                    for n,f in distance.distances:
                        d=f(doc_[1],doc[1])
                        verbose("{0} distance".format(n).ljust(30),
                                "{0:0.4f}".format(d))
                        feats.append(d)
                samples_.append(feats)
                classes_.append(ANS)
                   
            samples.append(samples_)
            classes.append(classes_)


            # save figures if requiered
            if opts.figures:
                data=np.zeros((len(docs)*len(docread.representations),
                              (len(docs)+1)*len(distance.distances)))
                for ix1 in range(len(docs)):
                    for ix2 in range(ix1,len(docs)):
                        for ixr in range(len(docread.representations)):
                            dis=0
                            for n,f in distance.distances:
                                ix2_=dis*(len(docs)+1)+ix2
                                ix1_=ixr*len(docs)+ix1
                                data[ix1_,ix2_]=f(docs[ix1][ixr][1],docs[ix2][ixr][1])
                                dis+=1
                for ix1 in range(len(docs)):
                    for ixr in range(len(docread.representations)):
                        dis=0
                        for n,f in distance.distances:
                            ix1_=ixr*len(docs)+ix1
                            ix2_=(dis+1)*(len(docs)+1)-1
                            data[ix1_,ix2_]=f(docreps[ixr][1],docs[ix1][ixr][1])
                            dis+=1
                fig,ax = plt.subplots()
                ax.pcolor(data, edgecolors='k', linewidths=2,cmap=plt.cm.Blues)
                plt.title("Distance visualization T. docs {0}".format(len(docs)))
                plt.show()
     


        # Initialization of ML
        Total_=0.0
        N_Acc_=0

        # leave-one-out problem
        info('Leave one oue one out')
        for i in range(len(samples)):
            info('Model for ',str(i))
            X_train = samples[:i]+samples[i+1:]
            X_train = list(itertools.chain(*X_train))
            X_test  = samples[i]
            Y_train = classes[:i]+classes[i+1:]
            Y_train = list(itertools.chain(*Y_train))
            Y_test  = classes[i]

            if opts.method.startswith('svm'):
                svc   = ML.svmtrain(X_train,Y_train)
                preds = ML.svmtest(svc,X_test)
            elif opts.method.startswith('avp'):
                ws    = ML.avptrain(X_train,Y_train,opts.iters)
                preds = ML.avptest(X_test,ws)
                
            for x,x_ in zip(preds,Y_test):
                if x==x_:
                    N_Acc_+=1
                Total_+=1
            verbose("Prediction "," ".join([posneg(x) for x in preds]))
            verbose("GS         "," ".join([posneg(x) for x in Y_test]))

        info('Accuracy : {0:04f}'.format(N_Acc_/Total_))

