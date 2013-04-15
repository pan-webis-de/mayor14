#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# ML methods
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

# ML libraries
import numpy as np
import random 
random.seed()

# Suppor vector machine
from sklearn import svm

# Linear programming
from cvxopt import matrix, solvers
import Weights as W

# Neuronal Networks
from pybrain.datasets            import ClassificationDataSet
#from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer,TanhLayer


def choice(x):
    if x<=0.5:
        return (0,x)
    else:
        return (1,x)

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
    solvers.options['show_progress'] = False
    sol=solvers.lp(c,A,B)
    return sol['x']

def lptest(xdata,ws):
    y=[]
    for x in xdata:
        y.append(choice(sum([x_*w for x_,w in zip(x,ws)])))
    return y


def svmtrain(xdata,ydata):
    xdata=np.array(xdata)
    ydata=np.array(ydata)
    svc = svm.SVR(
            C=5,
            kernel='linear',
            probability=True
        )
    svc.fit(xdata,ydata)
    return svc


def svmtest(svc,xdata,goal=None):
    xdata=np.array(xdata)
    #if goal:
    #    print goal
    #print [svc.predict(x) for x in xdata]
    return [choice(svc.predict(x)[0]) for x in xdata]


def avptrain(xdata,ydata,iters):
    ws=W.Weights()
    acc=W.Weights()
    total=0
    xydata=zip(xdata,ydata)
    for i in range(iters):
        random.shuffle(xydata)
        for x,y in xydata:
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

def anntrain(xdata,ydata):#,epochs):
    #print len(xdata[0])
    ds=SupervisedDataSet(len(xdata[0]),1)
    #ds=ClassificationDataSet(len(xdata[0]),1, nb_classes=2)
    for i,algo in enumerate (xdata):
        ds.addSample(algo,ydata[i])
    #ds._convertToOneOfMany( ) esto no
    net= FeedForwardNetwork()
    inp=LinearLayer(len(xdata[0]))
    h1=SigmoidLayer(1)
    outp=LinearLayer(1)
    net.addOutputModule(outp) 
    net.addInputModule(inp) 
    net.addModule(h1)
    #net=buildNetwork(len(xdata[0]),1,1,hiddenclass=TanhLayer,outclass=SoftmaxLayer)
    
    net.addConnection(FullConnection(inp, h1))  
    net.addConnection(FullConnection(h1, outp))

    net.sortModules()

    trainer=BackpropTrainer(net,ds)#, verbose=True)#dataset=ds,verbose=True)
    #trainer.trainEpochs(40)
    trainer.trainOnDataset(ds,40) 
    #trainer.trainUntilConvergence(ds, 20, verbose=True, validationProportion=0.15)
    trainer.testOnData()#verbose=True)
    #print 'Final weights:',net.params
    return net

def anntest(xdata,net):
    out=[]
    for dato in xdata:
        out.append(choice((net.activate(dato)[0])))
    return out 

def voted(preds):
    cs={0.0:0.0, 1.0:0.0}
    cs_={0.0:0, 1.0:0}
    for pred,val in preds:
        if pred==0.0:
            cs[pred]+=(0.5-val)
        else:
            cs[pred]+=(val-0.5)
        cs_[pred]+=1

    if cs_[0.0]==0:
        return "N"
    if cs_[1.0]==0:
        return "Y"
    if cs_[0.0]>=cs_[1.0]:
        return "Y"
    else:
        return "N"
