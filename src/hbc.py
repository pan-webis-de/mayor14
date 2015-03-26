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
from collections import Counter
from oct2py import octave
from oct2py.utils import Oct2PyError
octave.addpath('src/octave')

octave.timeout=60

class dotdict(dict):
    def __getattr__(self,attr):
        return self.get(attr)
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__

def muestreo(counter,reps,percentage=.80):
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
   
    for i in range(opts.nimpostors):
        for j in range(opts.ndocs):
            id_=pos[i*opts.nimpostors+j]
            for k in range(nknown):
                master_candidate={}
                doc=problems[ids_candidates[id_]+k]
                doc,text=docread.tag(doc[1][0][0][0],doc[1][0][0][1],opts.langugage)
                for repname in opts.reps:
                    try:
                        exec("f=docread.{0}".format(repname))
                        rep=f(doc,text,cutoff=cutoff,sw=sw)
                    except:
                        rep=Counter()
                    try:
                        master_candidate[repname].update(rep)
                    except KeyError:
                        master_candidate[repname]=Counter(rep)

                master_impostors.append(master_candidate)
    return master_impostors
 

def project_into_vectors(examples,full_voca,unknown,reps,nmost=100):
    vectors=[[] for e in examples]
    uvec=[]
    mass=[]
    N=len(examples)+1
    for rep in reps:
        full=Counter()
        for example in examples:
            full.update(example[rep])
            mass.append(sum(example[rep].values()))
        umass=sum(unknown[rep].values())
        full.update(unknown[rep])
        idx=[p[0] for p in full.most_common()[:200]]
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
            if mass[i]>0:
                arr=[1.0*example[rep][k]*idf[k] for k in idx]
            else:
                arr=[1.0*example[rep][k]*idf[k] for k in idx]
            vectors[i].append(arr)
        if umass>0:
           uvec.append([1.0*unknown[rep][k]*idf[k] for k in idx])
        else:
           uvec.append([1.0*unknown[rep][k]*idf[k] for k in idx])
    return [list(itertools.chain(*vec)) for vec in vectors], list(itertools.chain(*uvec))

codes=docread.codes

def hbc(example_vectors,unknown,nexamples,nks,opts):
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
    k=nexamples/nks*opts.ndocuments
    for i in range(k):
        n=opts.documents*nks
        d_i= np.matrix([[0.0 for x in x_0[:i*n]]+\
             [np.float(x) for x in x_0[i*n:(i+1)*n]]+\
             [0.0 for x in x_0[(i+1)*n:]]]).T
        d_is.append(np.linalg.norm(d_i,ord=1))
        r_is=y_-A_*d_i
        r_i=np.linalg.norm(r_is,ord=2)
        residuals.append(r_i)
    
    sci=(k*np.max(d_is)/np.linalg.norm(x_0,ord=1)-1)/(k-1)
    identity=np.argmin(residuals)
    scith=0.1
    if sci<scith:
        return 0.0
    else:
        if identity==(k-1):
            return 1.0
        else:
            return 0.0

def iterative_hbc(iters,example_vectors,unknown,nexamples,nks,opts):
    answer=False
    nanswers=0
    results=[]

    while not answer:
        if nanswers>4:
            results=[0.0 for i in range(iters)]
            break
        try:
            result=hbc(example_vectors,unknown,nexamples,nks,opts)
            results.append(result)
            nanswers+=1
        except Oct2PyError:
            nanswers+=1
            pass
        except TypeError:
            nanswers+=1
            pass

def process_corpus(problems,impostor_problems,opts=default_opts,mode="test",sw=[],verbose=lambda *a: None ):
	#Iterating over problems
        if opts.nmax>0:
            problems=problems[:opts.nmax]

        dumpfiles=[]
        if opts.dump:
            dumpfiles=[open('answers_{0}.dump'.format(iter),'w') 
                        for iter in range(opts.iters)]

        for id,(ks,uks) in problems:
            verbose( "Problem",id)
            master_author={}
            docs_author=[]
            master_unknown={}
            full_voca={}
            ks_=ks
            for filename,doc in ks:
                doc,text=docread.tag(filename,doc,opts.language)
                doc_author={}
                for repname in opts.reps:
                    #try:
                    exec("f=docread.{0}".format(repname))
                    rep=f(doc,text,cutoff=opts.cutoff,sw=sw)
                    #except:
                    #    rep=Counter()
                    doc_author[repname]=rep
                    try:
                        master_author[repname].update(rep)
                    except KeyError:
                        master_author[repname]=Counter(rep)
                    try:
                        full_voca[repname].update(rep)
                    except KeyError:
                        full_voca[repname]=Counter(rep)
                docs_author.append(doc_author)

            for filename,doc in uks:
                 doc,text=docread.tag(filename,doc,opts.language)
                 for repname in opts.reps:
                    try:
                        exec("f=docread.{0}".format(repname))
                        rep=f(doc,text,sw=sw,cutoff=opts.cutoff)
                    except:
                        rep=Counter()
                    try:
                        master_unknown[repname].update(rep)
                    except KeyError:
                        master_unknown[repname]=Counter(rep)
                    try:
                        full_voca[repname].update(rep)
                    except KeyError:
                        full_voca[repname]=Counter(rep)

            results=[]
            iters=opts.iters

            verbose("Master unknown",id,master_unknown)

            for iter in range(iters):
                verbose("Iter",iter)
                #Extracting Examples
                examples= []
                lens=[]

                # Getting impostors
                verbose('Total documents ',len(ks))
                master_impostors=get_master_impostors(id,len(ks),impostor_problems,opts,mode=mode,sw=sw)
                verbose('Total impostors ',len(master_impostors))

                # Sample impostors
                verbose("Sampling")
                for j,master_impostor in enumerate(master_impostors):
                     examples.append(muestreo(master_impostor,opts.reps,percentage=opts.percentag))

                for j in range(opts.documents):
                    for i in range(len(ks)):
                        doc_author=docs_author[i]
                        examples.append(muestreo(doc_author,opts.reps,percentage=opts.percentage))
                        lens.append(len(ks_))

                sample_unknown=muestreo(master_unknown,opts.reps,percentage=1.0)

                # Sparce algorithm
                # Proyecting examples into a vector
                verbose("Projectiong into vector")
                example_vectors,unknown=project_into_vectors(examples,full_voca,sample_unknown,opts.reps)
               



              
                if opts.dump:
                    print >> dumpfiles[iter], id, sum(results)/(iter+1)
            print(id, sum(results)/iters)
        for f in dumpfiles:
            f.close()
    

