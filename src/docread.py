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

from nlpcore import postagger, fulltagger


spaces=re.compile('\W+',re.UNICODE)
spaces_=re.compile('[ \t]+',re.UNICODE)
period=re.compile('[.;!?]',re.UNICODE)
rcapital=re.compile(u'[\u0391-\u03A9][^ ]+|[A-Z][^ ]+',re.UNICODE)
#rcapital=re.compile(r'[A-Z][^W]+',re.UNICODE)
rpar2 = re.compile(u'[.:].?\r?\n[A-Z]|[.:].?\r?\n[\u0391-\u03A9]',re.UNICODE)
rterm=re.compile('[.,]',re.UNICODE)
rpar = re.compile('\'''',re.UNICODE)
renter = re.compile('\r?\n',re.UNICODE)
renterer =re.compile('\r?\n',re.UNICODE)
#wordpunct=re.compile('\w+\W+',re.UNICODE)
wordpunct=re.compile(u'\W+',re.UNICODE)
rcoma=re.compile(r'\w+,',re.UNICODE)
rdot=re.compile(r'\w+\.',re.UNICODE)
rspc=re.compile(r'[/]',re.UNICODE)
rwspc=re.compile(r'\s',re.UNICODE)
rnumbers=re.compile(r'\d+',re.UNICODE)

# Codes for problems
codes={
    'en': {
        'essays': re.compile('^[^\w]*EE'),
        'novels': re.compile('^[^\w]*EN'),
        'all': re.compile('^[^\w]*E')
        },
    'nl': {
        'essays': re.compile('^[^\w]*DE'),
        'reviews': re.compile('^[^\w]*DR'),
        'all': re.compile('^[^\w]*D')
        },
    'gr': {
        'news': re.compile('^[^\w]*GR'),
        'all': re.compile('^[^\w]*GR')
        },
    'es': {
        'news': re.compile('^[^\w]*SP'),
        'all': re.compile('^[^\w]*SP')
        },
    'all': {
        'all': re.compile('.*')
    }
}



def none(docs,filename):
    return None

# Functions for representation extraction
def numbers(doc,sw=[]):
    wds = rnumbers.findall(doc)
    values=[x.encode('utf-8') for x in wds]
    doc=Counter(values)
    com=postprocess(doc)
    return doc,com,values

def numbers_size(doc,sw=[]):
    wds = rnumbers.findall(doc)
    values=[str(len(x)) for x in wds]
    doc=Counter(values)
    com=postprocess(doc)
    return doc,com,values

def capital(doc,sw=[]):
    wds = rcapital.findall(renter.sub(' ',doc))
    values=[x.encode('utf-8').lower() for x in wds]
    doc=Counter(values)
    com=postprocess(doc)
    return doc,com,values

def punct(doc,sw=[]):
    wds=wordpunct.findall(spaces_.sub('',renter.sub(' ',doc.lower())))
    values=[x.encode('utf-8') for x in wds]
    doc=Counter(values)
    com=postprocess(doc,ncutoff=0,ncommons=0)
    return doc,com,values

def bow(doc,sw=[]):
    wds = spaces.split(renter.sub(' ',doc.lower()))
    wds = preprocess(wds,sw)
    doc=Counter([x.encode('utf-8') for x in wds])
    com=postprocess(doc,ncommons=0,ncutoff=0,sw=sw)
    return doc,com,[x.encode('utf-8') for x in wds]

def stopwords(doc,sw=[]):
    wds = spaces.split(renter.sub(' ',doc.lower()))
    wds = [w for w in wds if w in sw]
    doc=Counter([x.encode('utf-8') for x in wds])
    com=postprocess(doc,ncommons=0,ncutoff=0,sw=sw)
    return doc,com,[x.encode('utf-8') for x in wds]


def prefix(doc,sw=[]):
    wds = spaces.split(renter.sub(' ',doc.lower()))
    wds = preprocess(wds,sw)
    doc=Counter([x.encode('utf-8')[:5] for x in wds if len(x)>5])
    com=postprocess(doc,ncommons=0,ncutoff=0,sw=sw)
    return doc,com,[x.encode('utf-8') for x in wds]

def sufix(doc,sw=[]):
    wds = spaces.split(renter.sub(' ',doc.lower()))
    wds = preprocess(wds,sw)
    doc=Counter([x.encode('utf-8')[-5:] for x in wds if len(x)>5])
    com=postprocess(doc,ncommons=0,ncutoff=0,sw=sw)
    return doc,com,[x.encode('utf-8') for x in wds]


def letters(doc,sw=[]):
    # Off
    wds = doc.lower()
    values=[x.encode('utf-8') for x in wds]
    doc=Counter(values)
    com=postprocess(doc)
    return doc,com,values

def coma(doc,sw=[]):
    wds = rcoma.findall(doc.lower())
    values=[x.encode('utf-8')[:-1] for x in wds]
    doc=Counter(values)
    com=postprocess(doc,ncutoff=0,ncommons=0,sw=sw)
    return doc,com,values

def dot(doc,sw=[]):
    wds = rdot.findall(doc.lower())
    values=[x.encode('utf-8')[:-1] for x in wds]
    doc=Counter(values)
    com=postprocess(doc,ncutoff=0,ncommons=0,sw=sw)
    return doc,com,values

def sqrbrackets(doc,sw=[]):
    wds = rspc.findall(doc)
    doc=Counter([x.encode('utf-8') for x in wds])
    com=postprocess(doc,ncutoff=0,ncommons=0)
    return doc,com,[x.encode('utf-8') for x in wds]

def whitespc(doc,sw=[]):
    wds = rwspc.findall(doc)
    doc=Counter([x.encode('utf-8') for x in wds])
    com=postprocess(doc,ncutoff=0,ncommons=0)
    return doc,com,[x.encode('utf-8') for x in wds]

def enter(doc,sw=[]):
    wds = renterer.findall(doc)
    doc=Counter([x.encode('utf-8') for x in wds])
    com=postprocess(doc,ncutoff=0,ncommons=0)
    return doc,com,[x.encode('utf-8') for x in wds]    

def bigram(doc,sw=[]):
    wds = spaces.split(renter.sub(' ',doc.lower()))
    wds = preprocess(wds,sw)
    
    bigram = zip(wds, wds[1:])
    values=["{0} {1}".format(x.encode('utf-8'),
                                    y.encode('utf-8')) for x, y in bigram]
    doc = Counter(values)
    com=postprocess(doc,ncutoff=0,ncommons=1)
    return doc,com,values

def bigramstop(doc,sw=[]):
    wds = [ x.encode('utf-8') for x in spaces.split(renter.sub(' ',doc.lower()))]
    
    bigram = zip(wds, wds[1:])
    values=["{0} {1}".format(x,y[:5]) for x, y in bigram

                                    if x in sw]
    doc = Counter(values)
    com=postprocess(doc,ncutoff=0,ncommons=0)
    return doc,com,values




def bigrampref(doc,sw=[]):
    wds = spaces.split(renter.sub(' ',doc.lower()))
    wds = preprocess(wds,sw)
    bigram = zip(wds, wds[1:])
    values=["{0} {1}".format(x.encode('utf-8')[:5],
                                    y.encode('utf-8')[:3]) for x, y in bigram]
    doc = Counter(values)
    com=postprocess(doc,ncutoff=0,ncommons=1)
    return doc,com,values

def bigramsuf(doc,sw=[]):
    wds = spaces.split(renter.sub(' ',doc.lower()))
    wds = preprocess(wds,sw)
    bigram = zip(wds, wds[1:])
    values=["{0} {1}".format(x.encode('utf-8')[-5:],
                                    y.encode('utf-8')[:3]) for x, y in bigram]
    doc = Counter(values)
    com=postprocess(doc,ncutoff=0,ncommons=1)
    return doc,com,values




def trigram(doc,sw=[]):
    wds = spaces.split(renter.sub(' ',doc.lower()))
    wds = preprocess(wds,sw)
    tri = zip(wds, wds[1:], wds[2:])
    values = ["{0} {1} {2}".format(x.encode('utf-8'),
                                    y.encode('utf-8'),
                                    z.encode('utf-8')) for x, y,z in tri]
    doc = Counter(values)

    com=postprocess(doc,ncutoff=0)
    return doc,com,values


def ngram(doc,sw=[],ngram=3):
    wds = [w.encode('utf-8') for w in spaces.split(renter.sub(' ',doc.lower()))]

    doc=Counter([])
    for n in range(ngram):
        args=[]
        pat=[]
        for j in range(n+1):
            args.append(wds[j:])
            pat.append('{{{0}}}'.format(j))
        val= zip(*args)
        values = [" ".join(pat).format(*v) for v in val]
        doc.update(values)

    com=postprocess(doc,sw=sw,ncutoff=5)
    return doc,com,values

def wordssntc(doc,sw=[]):
    wds = [str(len(spaces.split(w))/10) for w in period.split(renter.sub(' ',doc.lower()))]
    par = Counter(wds)
    com=postprocess(par,ncutoff=0,ncommons=0)
    return par,com,wds

def wordpar(doc,sw=[]):
    #pars = [x.strip() for x in rpar.split(doc.lower()) if x and len(x.strip())>0]
    pars = rpar2.split(doc.lower())
    par = Counter()
    #par['0']=len(pars)/10
    for k, p in enumerate(pars):
        wds = spaces.split(p)
        #par[str(k+1)]=len(wds)
        par[str(k-len(pars))]=len(wds)
    com=postprocess(par,ncutoff=0,ncommons=0)
    return par,com,[x.encode('utf-8') for x in pars]

def sntcpar(doc,sw=[]):
    #pars = [x.strip() for x in rpar.split(doc.lower()) if x and len(x.strip())>0]
    pars =rpar2.split(doc)
    par = Counter()
    #par['0']=len(pars)/10
    for k, p in enumerate(pars):
      par[str(k+1)]=1
    com=postprocess(par,ncutoff=0,ncommons=0)
    return par,com,[x.encode('utf-8') for x in pars]

# NEW features NAACL based on NLP
def token(doc,sw=[],ngram=5):
    labels=fulltagger.tag(doc)
    doc=Counter([])
    for n in range(ngram):
        args=[]
        pat=[]
        for j in range(n+1):
            args.append(labels[j:][1])
            pat.append('{{{0}}}'.format(j))
        val= zip(*args)
        values = [" ".join(pat).format(*v) for v in val]
        doc.update(values)

    com=postprocess(doc,ncutoff=0,ncommons=0)
    return labels,com,[u"{0}/{2}/{1}".format(
                            w.encode('utf-8'),
                            pos.encode('utf-8'),
                            lemma.encode('utf-8')) for w,pos,lemma in labels]

def preprocess(wrds,sw):
    wrds_=[]
    for wrd in wrds:
        if not wrd in sw:
            wrds_.append(wrd)
    return wrds_

def postprocess(doc,ncommons=0,ncutoff=0,sw=[]):
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
    ('letters',letters),   #X
    ('bigram',bigram),
    ('bigrampref',bigrampref),
    ('bigramstop',bigramstop),
    ('bigramsug',bigramsuf),
    ('trigram',trigram), 
    ('punctuation',punct), 
    ('wordssntc',wordssntc), 
    ('stopwords',stopwords), 
    ('numbers',numbers),
    ('numbers_size',numbers),
    ('coma',coma),
    ('dot',dot),           
    ('bow',bow),
    ('prefix',prefix),
    ('sufix',sufix),
    ('capital',capital),   
    ('sntcpar',sntcpar),   
    ('wordpar',wordpar),
    ('sntcpar',sntcpar),
    ('sqrbrackets',sqrbrackets),
    ('whitespc',whitespc),    #X
    ('enter',enter),          #X
    ('token',token)
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
        if code.match(line) is None:
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
