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
import Weights as W
from sklearn import svm
from sklearn import preprocessing
import random 
random.seed()

def svmtrain(xdata,ydata):
    xdata=np.array(xdata)
    ydata=np.array(ydata)
    svc = svm.SVC(kernel='poly',C=1.0,gamma=0.2)
    svc.fit(xdata,ydata)
    return svc

def svmtest(svc,xdata):
    xdata=np.array(xdata)
    return svc.predict(xdata) 


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
            x=list(enumerate(x))
            if ws.val(x)>0.5:
                y_=0
            else:
                y_=1
            if not y_==y:
                if y==0:
                    ws.plus(list(enumerate([1 for a in x])))
                else:
                    ws.minus(list(enumerate([1 for a in x])))
                acc.plus(list(ws.w.iteritems()))
                total+=1
    return ws

def avptest(xdata,ws):
    ydata=[]
    for x in xdata:
        if ws.val(list(enumerate(x)))>0.5:
            ydata.append(1)
        else:
            ydata.append(0)
    print ws.w
    return ydata


