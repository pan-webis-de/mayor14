#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Evaluation of pan13
# ----------------------------------------------------------------------
# Ivan Vladimir Meza-Ruiz/ ivanvladimir at turing.iimas.unam.mx
# 2013/IIMAS/UNAM
# Ángel Toledo
# 2013/FC/UNAM
# Paola Ledesma 
# 2013/ENAH
# Gibran Fuentes
# 2013/IIMAS/UNAM
# Gabriela Jasso
# 2013/FI/UNAM
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
import docread
import numpy


def calc_data(sample,results):
    tp=float(len([i for (i,j) in zip(sample,results) if i==j and i=='Y']))
    fn=float(len([i for (i,j) in zip(sample,results) if i!=j and j=='Y']))
    fp=float(len([i for (i,j) in zip(sample,results) if i!=j and j=='N']))
    tn=float(len([i for (i,j) in zip(sample,results) if i==j and j=='N']))
    if tp+fp > 0.0:
        tpr=float(tp*1.0/(tp+fn))
    else:
        tpr=0.0
    if tp+fn > 0.0:
        fpr=1-float(tn*1.0/(fp+tn))
    else:
        fpr=0.0
    return (round(tpr,3),round(fpr,3))

    
def calculate_answers(probs,threshold):
    answers=[]
    for prob in probs:
        if prob>=threshold:
            answers.append('Y')
        else:
            answers.append('N')
    return answers

def create_points(steps,probs,results):
    points=[]
    for i in range(steps+1):
        n_threshold=i*(1.0/steps)
        answers=calculate_answers(probs,n_threshold)
        data=calc_data(answers,results)
        points.append(data)
    return fix_points(points)


def fix_points(points):
    points=sorted(points,key=lambda points:points[1])
    points=sorted(points,key=lambda points:points[0])
    return points


def calculate_AUC(points):
    x,y=zip(*points)
    return 100*numpy.trapz(x,y)

def verbose(*args):
    if opts.verbose:
        print >> out, "".join(args)

def info(*args):
    print >> out, "".join(args)


def loadfile(filename):
    labeling={}
    with open(filename) as file:
        for line in file:
            line=line.strip()
            if len(line)==0:
                continue
            bits=line.split()
            labeling[bits[0]]=bits[1]
    return labeling

codes=docread.codes

# MAIN
if __name__ == "__main__":
    version="%prog 0.1"

    # Command line options
    p = argparse.ArgumentParser("Evaluation script for author identification")
    p.add_argument("GS",
            action="store", help="File with GS answers")
    p.add_argument("SYS",
            action="store", help="File with SYS answers")
    p.add_argument("-l","--language",default='all',
            action="store", dest="language",
            help="Language to process [all]")
    p.add_argument("-g","--genre",default='all',
            action="store", dest="genre",
            help="Genre to process [all]")
    p.add_argument("-o", "--output",default=None,
            action="store", dest="output",
            help="Output [STDOUT]")
    p.add_argument( "--verbose",
            action="store_true", dest="verbose",
            help="Verbose mode [Off]")
    opts = p.parse_args()

    # Parameters
    out = sys.stdout
    if opts.output:
        try:
            out = open(opts.output)
        except:
            p.error('Output parameter could not been open: {0}'\
                    .format(opts.output))

    gs = docread.loadanswers(opts.GS,code=codes[opts.language][opts.genre])
    sys = docread.loadanswers(opts.SYS,code=codes[opts.language][opts.genre])
    
    #probas = docread.loadproba(args[1])
    tp=0
    fp=0
    fn=0
    total=0
    yeas=0
    noes=0
    sin_contestar=0
    tpd={}
    fpd={}
    fnd={}
    totals={}
    keys={}
    recall={}
    lenguas_sin={}

    for g,l in gs.iteritems():
        # False negative, there is no anwer or prob is 0.5
        try:
            keys[g[:2]].append(g)
        except KeyError:        
            keys[g[:2]]=[g]
        
        try:
            totals[g[:2]]+=1
        except KeyError:
            totals[g[:2]]=1
            
        total=total+1
   
        if not sys.has_key(g) or sys[g]==0.5:
            fn+=1
            try:
                fnd[g[:2]]+=1
            except KeyError:
                fnd[g[:2]]=1
            sin_contestar=sin_contestar+1
            try:
                lenguas_sin[g[:2]]+=1
            except KeyError:
                lenguas_sin[g[:2]]=1
            continue

        # Checking the answer
        if sys[g]<0.5:
            res='N'
            noes+=1
        else:
            res='Y'
            yeas+=1
        
        if res==l:
            tp+=1
            try:
                tpd[g[:2]]+=1
            except KeyError:
                tpd[g[:2]]=1
        else:
            fp+=1
	    fn+=1
            try:
                fpd[g[:2]]+=1
            except KeyError:
                fpd[g[:2]]=1
	    try:
                fnd[g[:2]]+=1
            except KeyError:
                fnd[g[:2]]=1
    langs=set([])
    langs.update(tpd.keys())
    langs.update(fpd.keys())
    langs.update(fnd.keys())
		


	
    info('True positives : ',str(tp))
    info('False positives: ',str(fp))
    info('False negatives: ',str(fn))
    info('Without ans    : ',str(sin_contestar))
    info('Total          : ',str(total))
    info('Ys             : ',str(yeas))
    info('Ns             : ',str(noes))
    info('==========')
    info('Accuracy  : {0:3.3f}%'.format(100.0*tp/len(gs)))
    info('==========')
    if tp>0 or fp>0:
        pres=100.0*tp/(tp+fp)
    else:
        pres=0.0
    if tp>0 or fn>0:
        recall=100.0*tp/(tp+fn)
    else:
        recall=0.0
 

    keys_full=sys.keys()
    points=create_points(100,[sys[x] for x in keys_full],
                            [gs[x] for x in keys_full])
    auc=calculate_AUC(points)

    c=100.0*(1/float(total))*(tp+(sin_contestar*tp*1.0/float(total))) 
    info('Precision : {0:3.3f}%'.format(pres))
    info('Recall    : {0:3.3f}%'.format(recall))
    if pres> 0.0 and recall > 0.0:
        info('F1-score  : {0:3.3f}%'.format(2*pres*recall/(pres+recall)))
    else:
        info('F1-score  : {0:3.3f}%'.format(0.0))
    info('AUC       : {0:3.3f}%'.format(auc))
    info('c@1       : {0:3.3f}%'.format(c))
    info('Rank      : {0:3.3f}%'.format(c*auc/100))


    info('==========')
    indice=0
    for lang in langs:
        try:
            tp=tpd[lang]
        except KeyError:
            tp=0
        try:
            fp=fpd[lang]
        except KeyError:
            fp=0
        try:
            fn=fnd[lang]
        except KeyError:
            fn=0
        if tp>0 or fp>0:
            pres=100.0*tp/(tp+fp)
        else:
            pres=0.0
        if tp>0 or fn>0:
            recall=100.0*tp/(tp+fn)
        else:
            recall=0.0
  
        try:
            sin_contestar=lenguas_sin[lang]
        except KeyError:
            sin_contestar=0
        total=totals[lang]

        sys_lang=[sys[x] for x in keys[lang] if sys.has_key(x)]
        gs_lang=[gs[x] for x in keys[lang] if sys.has_key(x)]
        if len(sys_lang)>0:
            info('-----',lang)
            points=create_points(20,sys_lang,
                                gs_lang)
            auc=calculate_AUC(points)

            c=100.0*(1/float(total))*(tp+(sin_contestar*tp*1.0/float(total))) 
            info('Precision : {0:3.3f}%'.format(pres))
            info('Recall    : {0:3.3f}%'.format(recall))
            indice=indice+1
            if pres> 0.0 and recall > 0.0:
                info('F1-score  : {0:3.3f}%'.format(2*pres*recall/(pres+recall)))
            else:
                info('F1-score  : {0:3.3f}%'.format(0.0))
            info('AUC       : {0:3.3f}%'.format(auc))
            info('c@1       : {0:3.3f}%'.format(c))
            info('Rank      : {0:3.3f}%'.format(c*auc/100))
        




