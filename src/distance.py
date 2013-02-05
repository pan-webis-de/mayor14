#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Experiment defition manager
# ----------------------------------------------------------------------
# Paola Ledesma /
# 2012/ENAH
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

#import nltk


def jacard(A,B):
    A=set(A.elements())
    B=set(B.elements())
    return 1-len(A.intersection(B))*1.0/len(A.union(B))
 
def masi_distance (A, B):
    label1=set(A.elements())
    label2=set(B.elements())
    return 1 - float(len(label1.intersection(label2)))/float(max(len(label1),len(label2)))

def tanimoto(A,B,**args):
    vec1=set(A.elements())
    vec2=set(B.elements())
    
    d1d2 = [item for item in vec1 if item in vec2]
  
    if len(d1d2)  == 0: return 0.0
  
    return 1-float(len(d1d2))/ (len(vec1) + len(vec2) - len(d1d2))
	
def sorensen(A,B,**args):
    vec1=set(A.elements())
    vec2=set(B.elements())
 
    d1d2 =  len([ item  for item in vec1 if item in vec2 ])
  
    if len(vec1) + len(vec2) == 0:
        return 0.0
  
    return 1-float(2.0*d1d2 / (len(vec1) + len(vec2) ) )


distances=[("Jacard",jacard),
           ("Masi",masi_distance),
           ("Tanimoto",tanimoto),
           ("Sorensen",sorensen)]


