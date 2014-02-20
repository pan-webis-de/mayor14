#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Evaluation of pan13
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
import docread

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


# MAIN
if __name__ == "__main__":
    usage="""%prog gsfile sysfile

        Evaluates the labelling againt a Gold standard labelling

        gsfile : Gold standard label.ing
        sysfile: Sistem labelling


"""

    version="%prog 0.1"

    # Command line options
    p = optparse.OptionParser(usage=usage,version=version)
    p.add_option("-o", "--output",default=None,
            action="store", dest="output",
            help="Output [STDOUT]")
    p.add_option("-v", "--verbose",
            action="store_true", dest="verbose",
            help="Verbose mode [Off]")
    opts, args = p.parse_args()

    # Arguments 
    if not len(args) == 2:
        p.error('Wrong number of arguments')

    # Parameters
    out = sys.stdout
    if opts.output:
        try:
            out = open(opts.output)
        except:
            p.error('Output parameter could not been open: {0}'\
                    .format(opts.output))

    gs = docread.loadanswers(args[0])
    sys = docread.loadanswers(args[1])

    tp=0
    fp=0
    fn=0
    tpd={}
    fpd={}
    fnd={}
    recall={}

    for g,l in gs.iteritems():
        #TP
        try:
            sys[g]
        except KeyError:
            fn+=1
            try:
                fnd[g[:2]]+=1
            except KeyError:
                fnd[g[:2]]=1
            continue


        if l==sys[g]:
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
    info('True positives: ',str(tp))
    info('False positives: ',str(fp))
    info('False negatives: ',str(fn))
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
    info('Precision : {0:3.3f}%'.format(pres))
    info('Recall    : {0:3.3f}%'.format(recall))
    if pres> 0.0 and recall > 0.0:
        info('F1-score  : {0:3.3f}%'.format(2*pres*recall/(pres+recall)))
    else:
        info('F1-score  : {0:3.3f}%'.format(0.0))


    info('==========')
    langs=set([])
    langs.update(tpd.keys())
    langs.update(fpd.keys())
    langs.update(fnd.keys())
    for lang in langs:
        info('-----',lang)
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
        info('Precision : {0:3.3f}%'.format(pres))
        info('Recall    : {0:3.3f}%'.format(recall))
        if pres> 0.0 and recall > 0.0:
            info('F1-score  : {0:3.3f}%'.format(2*pres*recall/(pres+recall)))
        else:
            info('F1-score  : {0:3.3f}%'.format(0.0))





