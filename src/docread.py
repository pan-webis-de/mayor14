#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Experiment defition manager
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
# docread.py is free software: you can redistribute it and/or modify
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

import re
import sys
import os
import os.path
import codecs
from collections import Counter

spaces=re.compile('\W+',re.UNICODE)
rcapital=re.compile(r'[A-Z][A-Za-z]+',re.UNICODE)
rpar = re.compile('\.',re.UNICODE)
wordpunct=re.compile('\w+\W+',re.UNICODE)

def readdoc(filename):
    with codecs.open(filename,'r','utf-8') as fh:
        return  fh.read()

def prettyprint(filename):
    with codecs.open(filename,'r','utf-8') as fh:
        for line in fh:
            line=line.strip()
            print line.encode('utf-8')

def apply(f,filename):
    with codecs.open(filename,'r','utf-8') as fh:
        return f(fh.read().encode())

def capital(doc):
    wds = rcapital.findall(doc)
    doc=Counter([x.encode('utf-8') for x in wds])
    com=preprocess(doc,ncommons=0,ncutoff=1)
    return doc,com,[x.encode('utf-8') for x in wds]


def punct(doc):
    wds = wordpunct.findall(doc.lower())
    doc=Counter([x.encode('utf-8') for x in wds])
    com=preprocess(doc)
    return doc,com,[x.encode('utf-8') for x in wds]

def txt(doc):
    wds = spaces.split(doc.lower())
    doc=Counter([x.encode('utf-8') for x in wds])
    com=preprocess(doc)
    return doc,com,[x.encode('utf-8') for x in wds]

def bigram(doc):
    wds = spaces.split(doc.lower())
    bigram = zip(wds, wds[1:])
    doc = Counter(["{0} {1}".format(x.encode('utf-8'),
                                    y.encode('utf-8')) for x, y in bigram])
    com=preprocess(doc,ncommons=0,ncutoff=1)
    return doc,com,[x.encode('utf-8') for x in wds]

def trigram(filename):
    wds = spaces.split(doc.lower())
    tri = zip(wds, wds[1:], wds[2:])
    doc = Counter(["{0} {1} {2ç".format(x.encode('utf-8'),
                                    y.encode('utf-8'),
                                    z.encode('utf-8')) for x, y,z in tri])

    com=preprocess(doc,ncommons=0,ncutoff=1)
    return doc,com,tri


def par(doc):
    pars = rpar.split(doc.lower())
    par = Counter() 
    for k, p in enumerate(pars):
        wds = spaces.split(p)
        par[str(k)]=len(wds)/5
    com=preprocess(par,ncommons=0,ncutoff=0)
    return par,com,[x.encode('utf-8') for x in pars]

def preprocess(doc,ncommons=10,ncutoff=5):
    commons=[x for x,c in doc.most_common(ncommons)]
    cutoff=[x for x,c in doc.iteritems() if c <= ncutoff ]
    for c in commons:
        del doc[c]
    for c in cutoff:
        del doc[c]
    return commons

def paragraph(text):
  # [.!?][\s]+(?=[A-Z])
  sep = re.compile('\.')
  return sep.split(text)

representations=[
#    ('trigram',trigram),
    ('bigram',bigram),
    ('punctuation',punct),
    ('bog',txt),
    ('capital',capital),
    ('par',par)]


def problems(dirproblems_):
    return [(id,([(k,readdoc(k)) for k in ks],[(u,readdoc(u)) for u in uks])) \
                for id,(ks,uks) in dirproblems_ ]    

def dirproblems(dirname, rknown  =r"known.*\.txt",
                         runknown=r"unknown.*\.txt",ignore=[]):
    """Loads the directories containing problems"""
    dirnames=[(x,"{0}/{1}".format(dirname,x)) for x in os.listdir(dirname)  
                if not x in ignore and
                   os.path.isdir("{0}/{1}".format(dirname,x))]
    problems=[]
    for id,dirname in dirnames:
        problems.append((id,
                        dirproblem(dirname,rknown,runknown,ignore)))
    return problems


def dirproblem(dirname, rknown  =r"known.*\.txt",
                        runknown=r"unknown.*\.txt",ignore=[]):
    """Loads problem """
    r_known=re.compile(rknown)
    r_unknown=re.compile(runknown)
    known  =["{0}/{1}".format(dirname,x) for x in os.listdir(dirname) 
                        if not x in ignore and
                        r_known.match(x)]
    unknown=["{0}/{1}".format(dirname,x) for x in os.listdir(dirname)
                        if not x in ignore and
                        r_unknown.match(x)]
    return known,unknown


def loadanswers(filename,ignore=[]):
    """Loads answers file"""
    r_answer=re.compile(r"[^\w]*(\w*) (Y|N)$")
    answers={}
    for line in open(filename):
        line=line.strip()
        if len(line)==0:
            continue
        m=r_answer.match(line)
        if m:
            if not m.group(1) in ignore:
                answers[m.group(1)]=m.group(2)
    return answers
