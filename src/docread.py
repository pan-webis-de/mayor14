#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Experiment defition manager
# ----------------------------------------------------------------------
# Ivan Vladimir Meza-Ruiz/ ivanvladimir at turing.iimas.unam.mx
# 2012/IIMAS/UNAM
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
from collections import Counter

def txt(filename):
    with open(filename) as fh:
        wds = re.split('\W+', fh.read())
    doc=Counter(wds)
    return doc

def trigram(wds):
	tri = zip(wds, wds[1:], wds[2:])
    doc = Counter(tri)
    return doc

def dirproblems(dirname,rknown  =r"known.*\.txt",
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

def dirproblem(dirname,rknown  =r"known.*\.txt",
                         runknown=r"unknown.*\.txt",ignore=[]):
    r_known=re.compile(rknown)
    r_unknown=re.compile(runknown)
    known  =["{0}/{1}".format(dirname,x) for x in os.listdir(dirname) 
                        if not x in ignore and
                        r_known.match(x)]
    unknown=["{0}/{1}".format(dirname,x) for x in os.listdir(dirname)
                        if not x in ignore and
                        r_unknown.match(x)]
    return known,unknown


def loadanswers(filename):
    # Loading ingnore if exists
    r_answer=re.compile(r"[^\w]*(\w*) (Y|N)$")
    answers={}
    for line in open(filename):
        line=line.strip()
        if len(line)==0:
            continue
        m=r_answer.match(line)
        if m:
            answers[m.group(1)]=m.group(2)
    return answers
