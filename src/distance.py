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

#import nltk
from math import sqrt
from math import pow
import numpy as np

def jacard(A, B,gbl=None):
    A_=set(A.keys())
    B_=set(B.keys())
    commons = A_.intersection(B_)
    full = A_.union(B_)
    num=len(commons)*1.0
    den=len(full)
    if den==0:
        return 1.0
    else:
        return  1-num/den 


def jacard2(A, B,gbl=None):
    A_=set(A.keys())
    B_=set(B.keys())
    commons = A_.intersection(B_)
    full = A_.union(B_)
    num=len(commons)
    den=len(full)
    if den==0:
        return 0.88
    else:
        return  1-num/den 

def jacardw(A, B,gbl=None):
    A_=set(A.keys())
    B_=set(B.keys())
    commons = A_.intersection(B_)
    full = A_.union(B_)
    num=sum([min(A[x],B[x]) for x in commons])*1.0
    den=sum([A[x]+B[x] for x in full])
    if den==0:
        return 1.0
    else:
        return  1-num/den 


def h0(A, B,gbl=None):
    # variacion http://cmp.felk.cvut.cz/~chum/papers/chum_bmvc08.pdf
    commons = set(A.keys()).intersection(set(B.keys()))
    num=sum([min(A[x],B[x]) for x in commons])
    den=sum([max(A[x],B[x]) for x in commons])
    if den==0:
        return 0.66
    else:
        return num/den 


def masi(A, B,gbl=None):
    # Equivalent to overlap_
    A_=set(A.keys())
    B_=set(B.keys())
    commons = A_.intersection(B_)
    num=len(commons)*1.0
    den=max(len(A_),len(B_))
    if den==0:
        return 1.0
    else:
        return  1-num/den 

def masiw(A, B,gbl=None):
    # Equivalent to overlap_
    A_=set(A.keys())
    B_=set(B.keys())
    commons = A_.intersection(B_)
    num=sum([min(A[x],B[x]) for x in commons])*1
    den=max(sum([A[x] for x in A_]),sum([B[x] for x in B_]))
    if den==0:
        return 0.8
    else:
        return num/den 



def overlap(A, B,gbl=None):
    A = set(A.elements())
    B = set(B.elements())
    num = len(A.intersection(B)) * 1.0
    den = min(len(A), len(B))
    if den == 0:
        return 1.0
    else:
        return  1 - (num/den)

def overlapw(A, B,gbl=None):
    A_=set(A.keys())
    B_=set(B.keys())
    commons = A_.intersection(B_)
    num=sum([min(A[x],B[x]) for x in commons])*1.0
    den=min(sum([A[x] for x in A_]),sum([B[x] for x in B_]))
    if den==0:
        return 1.0
    else:
        return  1-num/den 


def ledesma(A, B,gbl=None):
    # Variación de Tanimoto
    A_=set(A.keys())
    B_=set(B.keys())
    commons = A_.intersection(B_)
    
    num=float(len(commons))
    den=(pow(len(A_),2) + (pow(len(B_),2) - len(commons)))
    if den==0:
        return 1.0
    else:
        return  1-num/den 

def ledesmaw(A, B,gbl=None):
    # Variación de Tanimoto
    A_=set(A.keys())
    B_=set(B.keys())
    commons = A_.intersection(B_)
    
    num=1.0*sum([A[x] + B[x] for x in commons])
    den=(pow(sum(A.values()),2) + (pow(sum(B.values()),2)))
    if den==0:
        return 1.0
    else:
        return  1-num/den 


def sorensen(A, B,gbl=None):
    A_=set(A.keys())
    B_=set(B.keys())
    commons = A_.intersection(B_)
    num=2.0*len(commons)
    den=len(A_)+len(B_)
    if den==0:
        return 1.0
    else:
        return  1-num/den 

def sorensenw(A, B,gbl=None):
    A_=set(A.keys())
    B_=set(B.keys())
    commons = A_.intersection(B_)
    full = A_.union(B_)
    num=sum([A[x]+B[x] for x in commons])*1.0
    den=sum([A[x]+B[x] for x in full])
    if den==0:
        return 1.0
    else:
        return  1-num/den 


def dot(a,b):	
	commons = set(a.keys()).intersection (set(b.keys()))
	return sum([a[k] * b[k] for k in commons])

def cosine(a,b,gbl=None):
    num=dot(a, b)
    den=sqrt(dot(a,a)) * sqrt(dot(b,b))

    if den==0:
        return 1.0
    else:
        return 1-num/den 


def manhattan(A,B,gbl=None):
    commons = set(A.keys()).union(set(B.keys()))
    AA=sum([A[a] for a in A.keys()])
    BB=sum([B[a] for a in B.keys()])
    print AA*BB
    print sum([abs(A[a]-B[a]) for a in commons])
    if AA*BB == 0.0:
        return 1.0
    return 1-sum([abs(A[a]-B[a]) for a in commons])/(AA*BB)

def mahalanobis(A,B,gbl=None):
    if not gbl:
        return 1.0
    if not gbl.has_key('instances'):
        return 1.0

    commons = list(set(A.keys()).union(set(B.keys())))
    AB=np.array([[ A.get(x,0)  for  x in commons],[ B.get(x,0)  
                    for  x in commons]])
    if AB.shape[1]==0:
        return 1.0
    cov=np.cov(AB.T)
    dis=np.sqrt(np.dot(np.dot(AB[0]-AB[1],cov),(AB[0]-AB[1]).T))
    AA=np.sqrt(np.dot(np.dot(AB[0],cov),(AB[0]).T))
    BB=np.sqrt(np.dot(np.dot(AB[1],cov),(AB[1]).T))
    if AA*BB == 0.0:
        return 1.0
    return dis/(AA*BB)


def euclidean(A,B,gbl=None):
    commons = set(A.keys()).union(set(B.keys()))
    AA=sqrt(sum([(A[a])**2 for a in A.keys()]))
    BB=sqrt(sum([(B[a])**2 for a in B.keys()]))
    if AA*BB == 0.0:
        return 0.88
    return 1-sqrt(sum([(A[a]-B[a])**2 for a in commons]))/(AA*BB)


def ochiai(A,B,gbl=None):
    commons = (set(A.keys()).intersection(set(B.keys())))
    AA = len(A)
    BB = len(B)
    if (sqrt(AA*BB)) == 0.0:
        return 0.8
    return (len(commons))/ (sqrt(AA*BB))


distances=[
#           ("Jacard",jacard),
            ("jacard2",jacard2),
#           ("Masi",masi),
#           ("Ledesma",ledesma),
#           ("Sorensen",sorensen),
#          ("Overlap", overlap),
# Recomendadas para generalidad
            ("Weighted Jacard",jacardw),
            ("Weighted Sorensen",sorensenw),
            ("Weighted Ledesma",ledesmaw),
            ('Weighted h0',h0),
            ("Weighted Massi",masiw),
            ("Euclidean", euclidean),     
            #("Overlap", overlapw),
           #("Manhattan", manhattan),
            ("Cosine", cosine),
            #("ochiai",ochiai),
           ]
