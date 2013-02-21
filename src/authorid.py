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
    if val<0.5:
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
            help="test|train|devel [test]")
    p.add_option("-i", "--iters",default=10,type="int",
            action="store", dest="iters",
            help="Number of iterations for avg [10]")
    p.add_option("", "--model",default="pan13.model",
            action="store", dest="model",
            help="Model to save training or to test with [None]")
    p.add_option("", "--method",default="lp",
            action="store", dest="method",
            help="lp|avp|svm [avp]")
    p.add_option("", "--known_pattern",default=r'known.*\.txt',
            action="store", dest="known",
            help="pattern for known files [known*.txt]")
    p.add_option("", "--unknown_pattern",default=r'unknown*.txt',
            action="store", dest="unknown",
            help="pattern for unknown file [unknown*.txt]")
    p.add_option("", "--show-figures", default=False,
            action="store_true", dest="showf",
            help="Shows figures [None]")
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

    if not opts.mode in ["train","test","devel"]:
        p.error('Mode argument not valid: devel, train  test')

    
    dirname = args[0]

    # Parameters
    out = sys.stdout
    if opts.output:
        try:
            out = open(opts.output)
        except:
            p.error('Output parameter could not been open: {0}'\
                    .format(opts.output))

    # Preparing for saving info
    if opts.figures or opts.showf:
        import numpy as np
        import matplotlib
        import matplotlib.pyplot as plt
        if opts.figures:
            if not os.path.exists(opts.figures):
                verbose("Creating directory for figures:",opts.figures)
                os.mkdir(opts.figures)
    

    verbose("Running in mode:",opts.mode)
    # Loading ingnore if exists
    _ignore=[]
    if os.path.exists('.ignore'):
        verbose('Loading files to ignore frm: .ignore')
        with open('.ignore') as file:
            for line in file:
                _ignore.append(line.strip())

        

    # load problems or problem
    problems=docread.dirproblems(dirname,opts.known,opts.unknown,_ignore)

    # Loading answers file only for DEVELOPMENT OR TRAINNING MODE
    if opts.mode.startswith("train") or opts.mode.startswith("devel"):
 
        if not len(args)==2:
            p.error("Answers needed for train mode")
        verbose('Loading answer file: {0}'.format(args[1]))
        answers = docread.loadanswers(args[1],_ignore)

        # Checking for consistency
        if not len(problems) == len(answers):
            p.error("Not match for number of problems({0}) and \
            answers({1})".format(len(problems),len(answers)))


    samples=[]
    classes=[]
    # Transforms documents into samples 
    for id,(ks,uks) in problems:
        verbose('Reading from : {0}'.format(id))
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
            # Creating answers only if TRAINING or DEVELPMENT
            if opts.mode.startswith("train") or opts.mode.startswith("devel"):
                info('Answer to unknown: {0}'.format(answers[id]))
                if answers[id].startswith('Y'):
                    ANS=0 # Close in distance
                else:
                    ANS=1 # Far in distance
                classes_.append(ANS)
        samples.append(samples_)
        classes.append(classes_)

        # Saving figures only if TRAINING or DEVELOPMENT
        if opts.mode.startswith("train") or opts.mode.startswith("devel"):
            # save figures if requiered
            if opts.figures or opts.showf:
                nproblem=1
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
                            data[ix1_,ix2_]=f(docreps_[ixr][1],docs[ix1][ixr][1])
                            dis+=1
                fig,ax = plt.subplots()
                ax.pcolor(data, edgecolors='k', linewidths=2,cmap=plt.cm.Blues)
                plt.title("Distance visualization T. docs {0} \n\
case {1}".format(len(docs),posneg(ANS)))
                if opts.figures:
                    plt.savefig("{0}/{1}.png".format(opts.figures,id))
                if opts.showf:
                    plt.show()
     
    # DEVELOPMENT OR TRAINNING MODE
    if opts.mode.startswith("train") or opts.mode.startswith("devel"):
 
        if opts.mode.startswith("devel"):
            # leave-one-out problem
            info('Leave one out setting for development')
            # Initialization of ML
            Total =0.0
            N_Acc =0
            Total_=0.0
            N_Acc_=0
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
                    #print " ".join(["{0:.3f}".format(w) for w in ws.w.values()])
                    preds = ML.avptest(X_test,ws)
                elif opts.method.startswith('lp'):
                    ws    = ML.lptrain(X_train,Y_train)
                    print " ".join(["{0:.3f}".format(w) for w in ws])
                    preds = ML.lptest(X_test,ws)
           
                res=ML.voted(preds)

                if res==answers[problems[i][0]]:
                    N_Acc+=1
                Total+=1

                for x,x_ in zip(preds,Y_test):
                    if x[0]==x_:
                        N_Acc_+=1
                    Total_+=1
                verbose("Predictions "," ".join(["{0}/{1:0.2}".format(posneg(x),y)
                                                for x,y in preds]))
                verbose("GSs         "," ".join([posneg(x) for x in Y_test]))
                verbose("Prediction  ",res)
                verbose("GS          ",answers[problems[i][0]])


            info('Accuracy over all decisions : {0:3.3f}%'.format(100.0*N_Acc_/Total_))
            info('Accuracy over problems : {0:3.3f}%'.format(100.0*N_Acc/Total))
        # Trainning model
        elif opts.mode.startswith("train"):
            import pickle
            
            X_train = samples
            X_train = list(itertools.chain(*X_train))
            Y_train = classes
            Y_train = list(itertools.chain(*Y_train))

            verbose("Trainning model")
            if opts.method.startswith('svm'):
                verbose("Creating a SVM")
                svc   = ML.svmtrain(X_train,Y_train)
                s     = pickle.dumps(svc)
            elif opts.method.startswith('avp'):
                verbose("Creating an Average Percetron model")
                ws    = ML.avptrain(X_train,Y_train,opts.iters)
                s     = pickle.dumps(ws)
            elif opts.method.startswith('lp'):
                verbose("Calculating a linear program")
                ws    = ML.lptrain(X_train,Y_train)
                s     = pickle.dumps(ws)

            verbose("Saving model into",opts.model)
            with open(opts.model,"w") as model:
                model.write(s)
    elif opts.mode.startswith("test"):
        import pickle
        with open(opts.model,"r") as model:
            s=model.read()
        for i in range(len(samples)):
            X_test  = samples[i]

            if opts.method.startswith('svm'):
                svc   = pickle.loads(s)
                preds = ML.svmtest(svc,X_test)
            elif opts.method.startswith('avp'):
                ws    = pickle.loads(s)
                preds = ML.avptest(X_test,ws)
            elif opts.method.startswith('lp'):
                ws    =  pickle.loads(s)
                preds = ML.lptest(X_test,ws)
            
            res=ML.voted(preds)
            info(problems[i][0]," {0} ".format(res))



    else:
        info("Error with mode",opts.mode)


 


