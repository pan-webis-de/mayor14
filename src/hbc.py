#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Homotopy based classification 
# ----------------------------------------------------------------------
# Ivan V. Meza
# 2015/IIMAS, México
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
from __future__ import print_function

import random
import docread
import numpy as np
import itertools
from oct2py.utils import Oct2PyError
from oct2py import octave
from collections import Counter


class dotdict(dict):
    def __getattr__(self,attr):
        return self.get(attr)
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__

def muestreo(counter,reps,percentage=1.0):
    final_count={}
    for rep in reps:
        list_counter=list(counter[rep].elements())
        random.shuffle(list_counter)
       
        size=len(list_counter)
        final_list=list_counter[0:int(size*percentage)]  
      
        final_count[rep]=Counter(final_list)  
    return final_count

default_opts= dotdict({
    'cutoff':5,
    'language':'eng',
    'nimpostors':10,
    'ndocs':5
})

def get_master_impostors(id,nknown,problems,opts=default_opts,sw=[],mode="test"):
    if mode.startswith("test"):
        id=id+"___"
    master_impostors=[]
    ids_candidates=[]
    for i,(id_,(ks,uks)) in enumerate(problems):
        if id != id_ and i < len(problems)-nknown:
            ids_candidates.append(i)
    pos=range(len(ids_candidates))
    random.shuffle(pos)

   
    master_impostors=[]
    for i in range(opts.nimpostors):
        for j in range(opts.ndocs):
            master_impostors.append(pos[i*opts.nimpostors+j])
    return master_impostors
 

def project_into_vectors(examples,full_voca,unknown,nks,reps,nmost=200):
    vectors=[[] for e in examples]
    uvec=[]
    mass=[]
    N=len(examples)+1
    for rep in reps:
        full=Counter()
        for example in examples:
            full.update(example[rep])
            mass.append(sum(example[rep].values()))
        full.update(unknown[rep])
        idx=[p[0] for p in full.most_common()[:nmost]]
        idf={}
        t=0
        for id_ in idx:
            t=0
            for example in examples:
                try:
                    example[rep][id_]
                    t+=1
                except KeyError:
                    pass
            try:
                unknown[id_]
                t+=1
            except KeyError:
                pass
            idf[id_]=np.log(1.0*abs(N)/abs(t))

        for i,example in enumerate(examples):
            if sum(example[rep].values()) > 0:
                arr=[1.0*example[rep][k]*idf[k]/sum(example[rep].values())/nks for k in idx]
            else:
                arr=[0.0 for k in idx]
            vectors[i].append(arr)

        if sum(unknown[rep].values()) > 0:
            arr=[1.0*unknown[rep][k]*idf[k]/sum(unknown[rep].values()) for k in idx]
        else:
            arr=[0.0 for k in idx]

        uvec.append(arr)
    return [list(itertools.chain(*vec)) for vec in vectors], list(itertools.chain(*uvec))

codes=docread.codes

def hbc(example_vectors,unknown,nexamples,nks,opts,scith=0.1):
    # Creating matrix A
    # First samples represent to author, rest impostors
    # Normalizing the data
    A=np.matrix(example_vectors)
    A_=A.T
    y=np.matrix(unknown)
    y_=y.T
    nu=0.0000001
    tol=0.0000001

    stopCrit=3
    x_0, nIter = octave.SolveHomotopy(A_, y_, 'lambda', nu, 'tolerance', tol, 'stoppingcriterion', stopCrit)

    # Calculating residuals
    residuals=[]
    d_is=[]
    k=nexamples/opts.ndocs
    for i in range(k):
        n=opts.ndocs
        d_i= np.matrix([[0.0 for x in x_0[:i*n]]+\
             [np.float(x) for x in x_0[i*n:(i+1)*n]]+\
             [0.0 for x in x_0[(i+1)*n:]]]).T
        d_is.append(np.linalg.norm(d_i,ord=1))
        r_is=y_-A_*d_i
        r_i=np.linalg.norm(r_is,ord=2)
        residuals.append(r_i)
   
    sci=(k*np.max(d_is)/np.linalg.norm(x_0,ord=1)-1)/(k-1)
    identity=np.argmin(residuals)
    if sci < scith:
        return 0.0
    else:
        if identity==(k-1):
            return 1.0
        else:
            return 0.0

def try_hbc(example_vectors,unknown,nexamples,nks,opts):
    answer=False
    result=0.0
    nanswers=0

    while not answer:
        if nanswers>4:
            result=0.0
            break
        try:
            result=hbc(example_vectors,unknown,nexamples,nks,opts)
            answer=True
        except Oct2PyError:
            nanswers+=1
            pass
        except TypeError:
            nanswers+=1
            pass
    return result

def process_corpus(problems,impostor_problems,opts=default_opts,mode="test",sw=[],verbose=lambda *a: None ):
    #Iterating over problems
    if opts.nmax>0:
        problems=problems[:opts.nmax]

    dumpfiles=[]
    if opts.dump:
        dumpfiles=[open('answers_{0}.dump'.format(iter),'w') 
                    for iter in range(opts.iters)]

    for id,(ks,uks) in problems:
        verbose("Problem",id)
        master_author={}
        docs_author=[]
        master_unknown={}
        full_voca={}

        masters=[]
    
        for filename,doc in uks:
            masters.append(docread.tag(filename,doc,opts.language))
        verbose("Master unknown",id,[(k,len(v)) for k,v in
                masters])
     
        for filename,doc in ks:
            masters.append(docread.tag(filename,doc,opts.language))

        verbose("Master known",id,[(k,len(v)) for k,v in
            masters[:1]])

        for iter in range(opts.iters):
            #Extracting Examples
            masters_=[x for x in masters]

            # Getting impostors
            master_impostors=get_master_impostors(id,len(ks),impostor_problems,opts=opts,mode=mode,sw=sw)
            masters_=masters_.extend(masters)


            for repname in opts.reps:
                exec("f=docread.{0}".format(repname))
                rep=f(masters,cutoff=opts.cutoff,sw=sw)

            # Sparce algorithm
            example_vectors,unknown=project_into_vectors(examples,full_voca,sample_unknown,len(ks),opts.reps)

            result=try_hbc(example_vectors,unknown,len(examples),len(ks),opts)
            results.append(result)

            if opts.dump:
                print >> dumpfiles[iter], id, sum(results)/(iter+1)
        print(id, sum(results)/opts.iters)
    for f in dumpfiles:
        f.close()


