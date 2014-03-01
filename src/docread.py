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
import os
import os.path
import codecs
from collections import Counter

spaces=re.compile('\W+',re.UNICODE)
rcapital=re.compile(u'[\u0391-\u03A9][^ ]+|[A-Z][^ ]+',re.UNICODE)
#rcapital=re.compile(r'[A-Z][^W]+',re.UNICODE)
rpar2 = re.compile(u'[.:].?\r?\n[A-Z]|[.:].?\r?\n[\u0391-\u03A9]',re.UNICODE)
rterm=re.compile('[.,]',re.UNICODE)
rpar = re.compile('\'''',re.UNICODE)
renter = re.compile('\r?\n',re.UNICODE)
renterer =re.compile('\n',re.UNICODE)
#wordpunct=re.compile('\w+\W+',re.UNICODE)
wordpunct=re.compile('[^ ]+[\[\]():"\'.,;?¿]',re.UNICODE)
rcoma=re.compile(r'\w+,',re.UNICODE)
rdot=re.compile(r'\w+\.',re.UNICODE)
rspc=re.compile(r'[/]',re.UNICODE)
rwspc=re.compile(r'\s',re.UNICODE)
rnumbers=re.compile(r'\d+',re.UNICODE)

# Codes for problems
codes={
    'en': {
        'essays': re.compile('^EE'),
        'novels': re.compile('^EN'),
        'all': re.compile('^E')
        },
    'nl': {
        'essays': re.compile('^DE'),
        'reviews': re.compile('^DR'),
        'all': re.compile('^D')
        },
    'gr': {
        'news': re.compile('^GR'),
        'all': re.compile('^GR')
        },
    'es': {
        'news': re.compile('^SP'),
        'all': re.compile('^SP')
        },
    'all': {
        'all': re.compile('.*')
    }
}





def prettyprint(filename):
    with codecs.open(filename,'r','utf-8') as fh:
        for line in fh:
            line=line.strip()
            print line.encode('utf-8')

def none(docs,filename):
    return None

# Functions for representation extraction
def numbers(doc,sw=[]):
    wds = rnumbers.findall(doc)
    values=[x.encode('utf-8') for x in wds]
    doc=Counter(values)
    com=preprocess(doc,ncutoff=1,ncommons=0)
    return doc,com,values

def capital(doc,sw=[]):
    wds = rcapital.findall(renter.sub(' ',doc))
    values=[x.encode('utf-8').lower() for x in wds]
    doc=Counter(values)
    com=preprocess(doc,sw=sw,ncutoff=0,ncommons=1)
    return doc,com,values

def punct(doc,sw=[]):
    wds = wordpunct.findall(renter.sub(' ',doc.lower()))
    values=[x.encode('utf-8')[:-1] for x in wds]
    doc=Counter(values)
    com=preprocess(doc,ncutoff=0,ncommons=1)
    return doc,com,values

def bow(doc,sw=[]):
    wds = spaces.split(renter.sub(' ',doc.lower()))
    doc=Counter([x.encode('utf-8') for x in wds])
    com=preprocess(doc,ncommons=0,ncutoff=0,sw=sw)
    return doc,com,[x.encode('utf-8') for x in wds]

def letters(doc,sw=[]):
    # Off
    wds = doc.lower()
    values=[x.encode('utf-8') for x in wds]
    doc=Counter(values)
    com=preprocess(doc)
    return doc,com,values

def coma(doc,sw=[]):
    wds = rcoma.findall(doc.lower())
    values=[x.encode('utf-8')[:-1] for x in wds]
    doc=Counter(values)
    com=preprocess(doc,ncutoff=0,ncommons=0,sw=sw)
    return doc,com,values

def dot(doc,sw=[]):
    wds = rdot.findall(doc.lower())
    values=[x.encode('utf-8')[:-1] for x in wds]
    doc=Counter(values)
    com=preprocess(doc,ncutoff=0,ncommons=0,sw=sw)
    return doc,com,values

def sqrbrackets(doc,sw=[]):
    wds = rspc.findall(doc)
    doc=Counter([x.encode('utf-8') for x in wds])
    com=preprocess(doc,ncutoff=0,ncommons=0)
    return doc,com,[x.encode('utf-8') for x in wds]

def whitespc(doc,sw=[]):
    wds = rwspc.findall(doc)
    doc=Counter([x.encode('utf-8') for x in wds])
    com=preprocess(doc,ncutoff=0,ncommons=0)
    return doc,com,[x.encode('utf-8') for x in wds]

def enter(doc,sw=[]):
    wds = renterer.findall(doc)
    doc=Counter([x.encode('utf-8') for x in wds])
    com=preprocess(doc,ncutoff=0,ncommons=0)
    return doc,com,[x.encode('utf-8') for x in wds]    

def bigram(doc,sw=[]):
    wds = spaces.split(renter.sub(' ',doc.lower()))
    bigram = zip(wds, wds[1:])
    values=["{0} {1}".format(x.encode('utf-8'),
                                    y.encode('utf-8')) for x, y in bigram]
    doc = Counter(values)
    com=preprocess(doc,ncutoff=0,ncommons=1)
    return doc,com,values

def trigram(doc,sw=[]):
    wds = spaces.split(renter.sub(' ',doc.lower()))
    tri = zip(wds, wds[1:], wds[2:])
    values = ["{0} {1} {2}".format(x.encode('utf-8'),
                                    y.encode('utf-8'),
                                    z.encode('utf-8')) for x, y,z in tri]
    doc = Counter(values)

    com=preprocess(doc,ncutoff=0)
    return doc,com,values

def wordpar(doc,sw=[]):
    #pars = [x.strip() for x in rpar.split(doc.lower()) if x and len(x.strip())>0]
    pars = rpar.split(doc.lower())
    par = Counter()
    #par['0']=len(pars)/10
    for k, p in enumerate(pars):
        wds = spaces.split(p)
        #par[str(k+1)]=len(wds)
        par[str(k-len(pars))]=len(wds)
    com=preprocess(par,ncutoff=0,ncommons=0)
    return par,com,[x.encode('utf-8') for x in pars]


def sntcpar(doc,sw=[]):
    #pars = [x.strip() for x in rpar.split(doc.lower()) if x and len(x.strip())>0]
    pars =rpar.split(doc)
    par = Counter()
    #par['0']=len(pars)/10
    for k, p in enumerate(pars):
      par[str(k+1)]=1
    com=preprocess(par,ncutoff=0,ncommons=0)
    return par,com,[x.encode('utf-8') for x in pars]



def preprocess(doc,ncommons=0,ncutoff=0,sw=[]):
    commons=[x for x,c in doc.most_common(ncommons)]
    cutoff=[x for x,c in doc.iteritems() if c <= ncutoff ]
    for c in commons:
        del doc[c]
    for c in cutoff:
        del doc[c]
    for c in sw:
        del doc[c]
    commons=doc.most_common(10)
    return commons

representations=[
    #('letters',letters),   #X
    ('bigram',bigram),
    ('trigram',trigram), 
    ('punctuation',punct), 
    ('numbers',numbers),
    ('coma',coma),
    ('dot',dot),           
    ('bow',bow),
    ('capital',capital),   
    ('wordpar',wordpar),
    ('sntcpar',sntcpar),
    ('sqrbrackets',sqrbrackets),
    #('whitespc',whitespc),    #X
    #('enter',enter),          #X
    ]


def problems(dirproblems_):
    return [(id,([(k,readdoc(k)) for k in ks],[(u,readdoc(u)) for u in uks])) \
                for id,(ks,uks) in dirproblems_ ]    

def dirproblems(dirname, rknown  =r"known.*\.txt",
                         runknown=r"unknown.*\.txt",ignore=[],code=re.compile('.*')):
    """Loads the directories containing problems"""
    dirnames=[(x,"{0}/{1}".format(dirname,x)) for x in os.listdir(dirname)  
                if not x in ignore and
                   code.match(x) and
                   os.path.isdir("{0}/{1}".format(dirname,x))]
    dirnames.sort()
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
    known.sort()
    unknown=["{0}/{1}".format(dirname,x) for x in os.listdir(dirname)
                        if not x in ignore and
                        r_unknown.match(x)]
    unknown.sort()
    return known,unknown

# Reading file functions
def readstopwords(filename):
    stopwords=[]
    with codecs.open(filename,'r','utf-8') as file:
        for line in file:
            line=line.strip()
            if len(line)>0 and not line[0]=='#':
                stopwords.append(line.encode('utf-8'))
    return stopwords


def readdoc(filename):
    try:
        with codecs.open(filename,'r','utf-8') as fh:
            return  fh.read()
    except UnicodeDecodeError:
        try:
            with codecs.open(filename,'r','ISO-8859-1') as fh:
                return fh.read()
        except UnicodeDecodeError:
            return ""



def loadanswers(filename,ignore=[],code=re.compile('.*')):
    """Loads answers file"""
    r_answer=re.compile(r"[^\w]*(\w*) +(.*)$")
    answers={}
    for line in open(filename):
        line=line.strip()
        if len(line)==0:
            continue
        if not code.match(line):
            continue
        m=r_answer.match(line)
        if m:
            if not m.group(1) in ignore:
                try:
                    answers[m.group(1)]=float(m.group(2))
                except ValueError:
                    answers[m.group(1)]=m.group(2)
                    

    return answers

def loadproba(filename,ignore=[]):
    """Loads probabilities file"""
    #r_answer=re.compile(r"[^\w]*(\w*) (Y|N)$")
    answers={}
    i=0
    for line in open(filename):
        line=line.strip()
        if len(line)==0 or not line.startswith("proba"):
            continue
       
        r_answer=line.split(' ')
	answers[i]=r_answer[1]
        i=i+1
    return answers
