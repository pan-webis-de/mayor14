#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Author ID main 
# ----------------------------------------------------------------------
# Ivan Vladimir Meza-Ruiz/ ivanvladimir at turing.iimas.unam.mx
# 2013/IIMAS/UNAM
# Paola Ledesma 
# 2013/ENAH
# Gibran Fuentes
# 2013/IIMAS/UNAM
# Gabriela Jasso
# 2013/FI/UNAM
# Ángel Toledo
# 2013/FC/UNAM
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
import math
import itertools
from collections import Counter
from collections import defaultdict

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

        Runs user author identification 

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
    p.add_option("", "--list",default=False,
            action="store_true", dest="list_info",
            help="Displays distances metrics and representations")
    p.add_option("-q", "--query",default=None,
            action="store", dest="query",
            help="Query for a document")
    p.add_option("", "--norm",default=False,
            action="store_true", dest="norm",
            help="Normalize vector space")
    p.add_option("", "--off",default=[],
            action="append", dest="off",
            help="distances or representations to turn off")
    p.add_option("-i", "--iters",default=10,type="int",
            action="store", dest="iters",
            help="Number of iterations for avg [10]")
    p.add_option("", "--model",default="pan13.model",
            action="store", dest="model",
            help="Model to save training or to test with [None]")
    p.add_option("", "--method",default="lp",
            action="store", dest="method",
            help="lp|avp|svm|ann [avp]")
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
    p.add_option("", "--stopwords", default="data/stopwords.txt",
            action="store", dest="stopwords",
            help="List of stop words [data/stopwords.txt]")
    p.add_option("", "--answers", default="Answers.txt",
            action="store", dest="answers",
            help="Answers file [Answers.txt]")
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

    # If asked to print information 
    if opts.list_info:
        verbose('List information')
        verbose('-- Available Distances Metrics')
        for distancen,f in distance.distances:
            verbose(distancen)

        verbose('-- Available Representations')
        for rep,f in docread.representations:
            verbose(rep)

        sys.exit(0)


    # -- Normal functioning

    # Preparing for saving info
    if opts.figures or opts.showf:
        import numpy as np
        import matplotlib.pyplot as plt
        if opts.figures:
            if not os.path.exists(opts.figures):
                verbose("Creating directory for figures:",opts.figures)
                os.mkdir(opts.figures)
    

    # Loading ignore if exists
    _ignore=[]
    if os.path.exists('.ignore'):
        verbose('Loading files to ignore frm: .ignore')
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



    # load problems or problem
    problems=docread.problems(
        docread.dirproblems(dirname,opts.known,opts.unknown,_ignore))

    # If asked to print information 
    if opts.query:
        verbose('Query information')
        for id,(ks,uks) in problems:
            for k in ks:
                if opts.query in k[0]:
                    verbose("--- {0} ---".format(k[0]))
                    verbose("--- original ---")
                    docread.prettyprint(k[0])

                    for n,f in docread.representations:
                        if n in opts.off:
                            continue
                        rep,c,pars=f(k[1],sw=stopwords)
                        verbose("--- {0} partition ---".format(n))
                        print >> out, "\n:: ".join(pars)
                        verbose("--- {0} ---".format(n))
                        for key,v in rep.most_common():
                            verbose('{0} {1}'.format(key.ljust(45),v))

         
            for u in uks:
                if opts.query in u[0]:
                    verbose("--- {0} ---".format(u[0]))
                    verbose("--- original ---")
                    docread.prettyprint(u[0])

                    for n,f in docread.representations:
                        if n in opts.off:
                            continue
                        rep,ci,pars=f(k[1],sw=stopwords)
                        verbose("--- {0} partition ---".format(n))
                        print >> out, "\n:: ".join(pars)
                        verbose("--- {0} ---".format(n))
                        for key,v in rep.most_common():
                            verbose('{0} {1}'.format(key.ljust(45),v))


        sys.exit(0)
    

    verbose("Running in mode:",opts.mode)
    # Loading answers file only for DEVELOPMENT OR TRAINNING MODE
    if opts.mode.startswith("train") or opts.mode.startswith("devel"):
        if len(args)==2:
            answers_file= args[1]
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
    # Transforms documents into samples 
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

        # Load knowns 
        docs = []
        for k in ks:
            docreps=[]
            for rep,f in docread.representations:
                if rep in opts.off:
                    continue
                docreps.append((rep,f(k[1],stopwords)))
            docs.append(docreps)

        # Extract globals counts of known 
        docrepg={}
        insrepg={} # saves for unknowns the instances of counts per key
        docwords=Counter()
        for idoc,docreps in enumerate(docs):
            for doc in docreps:
                # Counts per document 
                try:
                    docrepg[doc[0]].update(doc[1][0])
                except KeyError:
                    docrepg[doc[0]]=Counter(doc[1][0])
                # Instances per document
                try:
                    insrepg[doc[0]]
                except KeyError:
                    insrepg[doc[0]]={}
                for k,v in doc[1][0].iteritems():
                    try:
                        insrepg[doc[0]][k].append(v)
                    except:
                        insrepg[doc[0]][k]=[v]
                            
                docwords.update(doc[1][0].keys())

        verbose('Loading files')
        samples_=[]
        classes_=[]

        for idoc,docreps in enumerate(docs):
            verbose('Comparing with: {0}'.format(ks[idoc][0]))
            feats=[]
            commons=Counter()
            for doc,doc_ in zip(docreps,docreps_): 
                verbose("-- {0} --".format(doc_[0]))
                for n,f in distance.distances:
                    if n in opts.off:
                        continue
                    # Normalizing
                    if opts.norm:
                        A=defaultdict(int)
                        B=defaultdict(int)
                        try:
                            mw_= doc_[1][1][0][1]
                        except IndexError:
                            mw_=1
                        try:
                            mw = doc[1][1][0][1]
                        except IndexError:
                            mw=1

                        idf=math.log(len(docreps))*1.0
                        idf_=math.log(1)*1.0
                        # Normalization tf
                        # tf logaritmith
                        A.update([(k,(1.0+math.log(v)))
                                for k,v in doc_[1][0].items() if v > 0])
                        B.update([(k,(1.0+math.log(v)))
                                for k,v in doc[1][0].items() if v > 0])
                    else:
                        A=doc_[1][0]
                        B=doc[1][0]
                    d=f(A,B,gbl={'instances':insrepg[doc[0]]})
                    verbose("{0} distance".format(n).ljust(30),
                            "{0:0.4f}".format(d))
                    feats.append(d)
                commons.update(doc[1][1])
            _tmp=[feats,0,0]
            # Figures out the language by common words
            if commons['the']>=1:
                _tmp[1]=feats
                _tmp[2]=[0.0 for x in feats]
            elif commons['el']>=1:
                _tmp[1]=feats
                _tmp[2]=[0.0 for x in feats]
            else:
                _tmp[2]=feats
                _tmp[1]=[0.0 for x in feats]

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
        samples.append(samples_)
        classes.append(classes_)

        # Saving figures only if TRAINING or DEVELOPMENT
        if opts.mode.startswith("train") or opts.mode.startswith("devel"):
            distances=[d for d in distance.distances if not d in opts.off]
            representations=[d for d in docread.representations if not d in opts.off]
            # save figures if requiered
            if opts.figures or opts.showf:
                nproblem=1
                xtick_lbs = range((len(docs)+1)*len(distances))
                ytick_lbs = range(len(docs)*len(representations))
                data=np.zeros((len(docs)*len(representations),
                              (len(docs)+1)*len(distances)))
                for ix1 in range(len(docs)):
                    for ix2 in range(ix1,len(docs)):
                        for ixr in range(len(representations)):
                            dis=0
                            for n,f in distances:
                                ix2_=dis*(len(docs)+1)+ix2
                                ix1_=ixr*len(docs)+ix1
                                data[ix1_,ix2_]=f(docs[ix1][ixr][1][0],
                                                  docs[ix2][ixr][1][0])
                                xtick_lbs[ix2_]="Doc {0}".format(ix2)
                                ytick_lbs[ix1_]="Doc {0}".format(ix1)
                                dis+=1
                for ix1 in range(len(docs)):
                    for ixr in range(len(representations)):
                        dis=0
                        for n,f in distances:
                            ix1_=ixr*len(docs)+ix1
                            ix2_=(dis+1)*(len(docs)+1)-1
                            data[ix1_,ix2_]=f(docreps_[ixr][1][0],
                                              docs[ix1][ixr][1][0])
                            xtick_lbs[ix2_]="Unk".format(ix2)
                            dis+=1
                fig,ax = plt.subplots()
                ax.pcolor(data, edgecolors='k', linewidths=2,cmap=plt.cm.Blues)
                xtick_lcs = np.array([.5+x for x in range((len(docs)+1)*\
                            len(distances))])

                ytick_lcs = np.array([.5+x for x in range(len(docs)*\
                            len(representations))])
                xtick_lbs = np.array(xtick_lbs)
                ytick_lbs = np.array(ytick_lbs)
                plt.xticks(xtick_lcs,xtick_lbs,rotation='vertical')
                plt.yticks(ytick_lcs,ytick_lbs)
                plt.title("Distance visualization {0} (N. docs {1}) \n\
case {2}".format(id,len(docs),posneg(ANS)))
                if opts.figures:
                    plt.savefig("{0}/{1}.png".format(opts.figures,id))
                if opts.showf:
                    plt.show()
     
    # DEVELOPMENT OR TRAINNING MODE
    if opts.mode.startswith("train") or opts.mode.startswith("devel"):
        tp=0.0
        fp=0.0
        fn=0.0
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
                    preds = ML.svmtest(svc,X_test,Y_test)
                elif opts.method.startswith('avp'):
                    ws    = ML.avptrain(X_train,Y_train,opts.iters)
                    #print " ".join(["{0:.3f}".format(w) for w in ws.w.values()])
                    preds = ML.avptest(X_test,ws)
                elif opts.method.startswith('ann'):
                    ws    = ML.anntrain(X_train,Y_train)#,opts.iters)
                    preds = ML.anntest(X_test,ws)
                elif opts.method.startswith('lp'):
                    try:
                        ws    = ML.lptrain(X_train,Y_train)
                        print " ".join(["{0:.3f}".format(w) for w in ws])
                        preds = ML.lptest(X_test,ws)
                    except TypeError:
                        print "ERROR NO MODEL"
                        preds = ML.lptest(X_test,[(1.0/15) for x in X_test[0]])
           
                res=ML.voted(preds)

                if res==answers[problems[i][0]]:
                    pref=""
                    N_Acc+=1
                    tp+=1
                else:
                    if res=='':
                        fn+=1
                    else:
                        fp+=1
                    pref="**"
                Total+=1

                for x,x_ in zip(preds,Y_test):
                    if x[0]==x_:
                        N_Acc_+=1
                    Total_+=1
                verbose(pref,"Model       ",problems[i][0])
                verbose(pref,"Predictions "," ".join(["{0}/{1:0.2}".format(posneg(x),y)
                                                for x,y in preds]))
                verbose(pref,"GSs         "," ".join([posneg(x) for x in Y_test]))
                verbose(pref,"Prediction  ",res)
                verbose(pref,"GS          ",answers[problems[i][0]])


            info('Accuracy over all decisions : {0:3.3f}%'.format(100.0*N_Acc_/Total_))
            info('Accuracy over problems : {0:3.3f}%'.format(100.0*N_Acc/Total))
            pres=100.0*tp/(tp+fp)
            recall=100.0*tp/(tp+fn)
            info('Precision : {0:3.3f}%'.format(pres))
            info('Recall    : {0:3.3f}%'.format(recall))
            info('F1-score  : {0:3.3f}%'.format(2*pres*recall/(pres+recall)))
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
            elif opts.method.startswith('ann'):
                verbose("Calculating an artificial neural network")
                ws = ML.anntrain(X_train,Y_train)
                s = pickle.dumps(ws)
            elif opts.method.startswith('lp'):
                verbose("Calculating a linear program")
                ws    = ML.lptrain(X_train,Y_train)
                s     = pickle.dumps(ws)

            verbose("Saving model into ",opts.model)
            with open(opts.model,"w") as model:
                model.write(s)
    # TEST model
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

                for x in X_test:
                    verbose((" ".join([str(x_*w) for x_,w in zip(x,ws)])))


            elif opts.method.startswith('ann'):
                ws    =  pickle.loads(s)
                preds = ML.anntest(X_test,ws)
            
            res=ML.voted(preds)
            info(problems[i][0]," {0} ".format(res))
            verbose("Predictions "," ".join(["{0}/{1:0.6}".format(posneg(x),y)
                                                for x,y in preds]))



    else:
        info("Error with mode",opts.mode)


 


