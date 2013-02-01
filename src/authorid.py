#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Distance metrics
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

import optparse
import sys
import os
import nltk
import numpy

# Local imports
import docread
import distance
import masi
import binary
import tanimoto
import sorensen


def verbose(MSG):
    if opts.verbose:
        print >> out, MSG


# MAIN
if __name__ == "__main__":
    usage="""%prog [options] dir doc

        Runs user identification 

        dir   : Directory with author examples
        doc   : Document to analyse 
"""

    version="%prog 0.1"

    # Command line options
    p = optparse.OptionParser(usage=usage,version=version)
    p.add_option("-o", "--output",default=None,
            action="store", dest="output",
            help="Output [STDOUT]")
    p.add_option("-t", "--type",default='txt',
            action="store", dest="type",
            help="txt [txt]")
 
    p.add_option("-v", "--verbose",
            action="store_true", dest="verbose",
            help="Verbose mode [Off]")
    opts, args = p.parse_args()

    # Arguments 
    if not len(args) is 2:
        p.error('Wrong number of arguments')

    dirname = args[0]
    docname = args[1]

    # Parameters
    out = sys.stdout
    if opts.output:
        try:
            out = open(opts.output)
        except:
            p.error('Output parameter could not been open: {0}'\
                    .format(opts.output))

    # Loading documents
    if opts.type.startswith('txt'):
        verbose('Opening: {0}'.format(docname))
        doc=(docname,docread.txt(docname))

    try:
        filenames=[x for x in os.listdir(dirname) if x.endswith(opts.type)]
    except:
        p.error('Error with dir argument: {0}'.format(dirname))
 
    docs=[]
    for filename in filenames:
        filename='{0}/{1}'.format(dirname,filename)
        if opts.type.endswith('txt'):
            verbose('Opening: {0}'.format(filename))
            docs.append((filename,docread.txt(filename)))
        
  
    # post process
 
    # Comparing documents
    bowbinary_doc=set(doc[1])
    verbose('Starting comparison')
    for doc_ in docs:
        bowbinary_doc_=set(doc_[1])
        print >> out, "{0} vs {1}".format(doc[0],doc_[0])
        print >> out, distance.jacard(bowbinary_doc,bowbinary_doc_)
        print >> out, masi.masi_distance(bowbinary_doc,bowbinary_doc_)
        print >> out, binary.binary_distance(bowbinary_doc,bowbinary_doc_)
        print >> out, tanimoto.tanimoto(bowbinary_doc,bowbinary_doc_)
        print >> out, sorensen.sorensen(bowbinary_doc,bowbinary_doc_)
