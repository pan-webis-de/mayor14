#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# ML methods
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

# ML libraries
import numpy as np
from sklearn import svm
from sklearn import preprocessing
import random 
random.seed()

from cvxopt import matrix, solvers
import Weights as W

def choice(x):
    if x>0.5:
        return (1.0,x)
    else:
        return (0.0,x)

def lptrain(xdata,ydata):
    A=[[] for x in xdata[0]]
    # Constrains for linear program
    for ix in range(len(xdata)):
        for iy in range(len(xdata[0])):
            # Adding constrains for alpha < 0.5 
            if ydata[ix]==0:
                A[iy].append(xdata[ix][iy])
                A[iy].append(-xdata[ix][iy])
            else:
            # Adding constrains for alpha > 0.5 
                A[iy].append(-xdata[ix][iy])
                A[iy].append(xdata[ix][iy])
    # Adding constrains for 0.0 < alpha < 1.0 
    for iy in range(len(xdata[0])):
        for iy_ in range(len(xdata[0])):
            if iy==iy_:
                A[iy].append(-1.0)
                A[iy].append(1.0)
            else:
                A[iy].append(0.0)
                A[iy].append(0.0)
    A=matrix(A)
    B=[]
    # Adding constrains
    for y in ydata:
        if y==0.0:
            B.append(0.5)
            B.append(0.0)
        else:
            B.append(-0.5)
            B.append(1.0)
    for y in range(len(xdata[0])):
        B.append(0.0)
        B.append(1.0)

    B=matrix(B)
    c=matrix([1.0 for x in xdata[0]])
    sol=solvers.lp(c,A,B)
    return sol['x']

def lptest(xdata,ws):
    y=[]
    for x in xdata:
        y.append(choice(sum([x_*w for x_,w in zip(x,ws)])))
    return y


def svmtest(svc,xdata):
    xdata=np.array(xdata)
    return svc.predict(xdata) 


def svmtrain(xdata,ydata):
    xdata=np.array(xdata)
    ydata=np.array(ydata)
    svc = svm.SVC(kernel='rbf',C=0.001,gamma=0.001,probability=True)
    svc.fit(xdata,ydata)
    return svc


def svmtest(svc,xdata):
    xdata=np.array(xdata)
    return [(x,svc.predict_proba(x)[0][x]) for x in svc.predict(xdata)]


def avinit(filename):
    # Loading weights or initializing
    if filename:
        # TODO load weights when given file
        pass

def avptrain(xdata,ydata,iters):
    ws=W.Weights()
    acc=W.Weights()
    total=0
    xydata=zip(xdata,ydata)
    for i in range(iters):
        random.shuffle(xydata)
        for x,y in xydata:
            x_total=sum(x)
            x=list(enumerate(x))
            score=ws.val(x)
            if score>0.5:
                y_=1
            else:
                y_=0
            if not y_==y:
                if y==0:
                    ws.minus(list(enumerate([.1*val for ix,val in x])))
                else:
                    ws.plus(list(enumerate([.1*val for ix,val in x])))
                acc.plus(list(ws.w.iteritems()))
                total+=1
    return ws

def avptest(xdata,ws):
    y=[]
    for x in xdata:
        y.append(choice(ws.val(list(enumerate(x)))))
    return y



