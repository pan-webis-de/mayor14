#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Author ID main 
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

# System libraries
import optparse
import sys
import os
import os.path
import re
import codecs
import shutil
import nltk

from urllib import urlopen
from collections import defaultdict

typeproblems=['original']

def minimum(line):
    if line.startswith('Fax'):
        return False
    return len(line)>100
    

def extract_links(line,opts={}):
    line=line.strip()
    if not len(line)>0:
        return None
    if line.startswith('#'):
        return None
    bits=line.split(u';')
    # TODO: return year
    url = bits[1].encode('utf-8')    
    html = urlopen(url).read()    
    raw = "\n".join(filter(minimum,
                    [line.strip() for line in  nltk.clean_html(html).splitlines()]))
    return (bits[2].encode('utf-8'),(bits[0].encode('utf-8'), # LANG
                                     raw  # html
                                    )
            ) 
        

# MAIN
if __name__ == "__main__":
    usage="""%prog [options] [linkfiles] 

        Downloads corpus from internet

        linkfile   : File with links
"""

    version="%prog 0.1"

    # Command line options
    p = optparse.OptionParser(usage=usage,version=version)
    p.add_option("-o", "--output",default=None,
            action="store", dest="output",
            help="Output [STDOUT]")
    p.add_option("", "--odir",default="data/linkcorpus",
            action="store", dest="odir",
            help="Output directory [data/linkcorpus]")
    p.add_option("-v", "--verbose",
            action="store_true", dest="verbose",
            help="Verbose mode [Off]")
    opts, args = p.parse_args()

    # Arguments 
    if not len(args) > 0:
        p.error('Wrong number of arguments')


    dirname = args[0]

    # Parameters
    output = sys.stdout
    if opts.output:
        try:
            output = open(opts.output)
        except:
            p.error('Output parameter could not been open: {0}'\
                    .format(opts.output))

    if opts.verbose:
        def verbose(*args):
            print >> output, "".join([str(x) for x in args])
    else:
        verbose = lambda *a: None 


    if not os.path.exists(opts.odir):
        verbose('Creating output dir',opts.odir)
        os.mkdir(opts.odir)
    else:
        verbose('Deleting content of output dir ',opts.odir)
        shutil.rmtree(opts.odir)
        os.mkdir(opts.odir)
        

    cproblems=defaultdict(int)
    answers=[]
    for linkfilename in args:
        with codecs.open(linkfilename,'r','utf-8') as linkfile:
            authors=defaultdict(list)
            authors_= [x for x in map(extract_links,linkfile) if x]
            for name,info in authors_:
                if name:
                    authors[name].append(info)

            for name,info in authors.iteritems():
                if len(info)>1:
                    verbose('Creating problems for ',name)
                else:
                    verbose('Not enough documents for ',name)
                    continue
                # Create original problem
                if 'original' in typeproblems:
                    lang=info[0][0]
                    ID="{0}{1:02}".format(
                            lang.upper(),
                            cproblems[lang])
                    os.mkdir("{0}/{1}".format(
                            opts.odir,ID))
                    nknown=1
                    # Generating KNOWNS
                    for n,(lang,txt) in enumerate(info[:-1]):
                        namefile_="known{0:02}.txt".format(n)
                        namefile="{0}/{1}/{2}".format(opts.odir,ID,namefile_)
                        with open(namefile,'w') as known:
                            print >> known, txt
                    namefile_="unknown.txt"
                    namefile="{0}/{1}/{2}".format(opts.odir,ID,namefile_)
                    with open(namefile,'w') as unknown:
                        print >> unknown, info[-1][1]
                    answers.append((ID,'Y'))
                    cproblems[lang]+=1

    namefile="{0}/Answers.txt".format(opts.odir)
    with open(namefile,'w') as ans:
        for ID,a in answers:
            print >> ans, "{0} {1}".format(ID,a)

            
