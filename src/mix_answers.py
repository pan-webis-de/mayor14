#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Evaluation of pan13
# ----------------------------------------------------------------------
# Ivan Vladimir Meza-Ruiz/ ivanvladimir at turing.iimas.unam.mx
# 2013/IIMAS/UNAM
# Ángel Toledo
# 2013/FC/UNAM
# Paola Ledesma 
# 2013/ENAH
# Gibran Fuentes
# 2013/IIMAS/UNAM
# Gabriela Jasso
# 2013/FI/UNAM
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

# System libraries
import argparse
import sys
import docread
import numpy
from os.path import basename

import yaml

codes=docread.codes

# MAIN
if __name__ == "__main__":
    version="%prog 0.1"

    # Command line options
    p = argparse.ArgumentParser("Evaluation script for author identification")
    p.add_argument("Answers",nargs='+',
            action="store", help="File answers files")
    p.add_argument("-c", "--conf",default='data/mix.conf',
            action="store", dest="conf",
            help="Configuration file [data/mix.conf]")
    p.add_argument("-o", "--output",default=None,
            action="store", dest="output",
            help="Output [STDOUT]")
    p.add_argument( "--verbose",
            action="store_true", dest="verbose",
            help="Verbose mode [Off]")
    opts = p.parse_args()

    # Parameters
    out = sys.stdout
    if opts.output:
        try:
            out = open(opts.output)
        except:
            p.error('Output parameter could not been open: {0}'\
                    .format(opts.output))


    with open(opts.conf, 'r') as stream:
        conf=yaml.load(stream)

    final={}
    for answersfile in opts.Answers:
        key_word=basename(answersfile)
        ans = docread.loadanswers(answersfile)
        for k,v in ans.iteritems():
            try:
                final[k]+=v*conf[key_word][k[:2]]
            except KeyError:
                final[k]=v*conf[key_word][k[:2]]

    for k,v in final.iteritems():
        print k, "{0:0.3f}".format(v)


