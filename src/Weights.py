#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# weights class
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

from collections import Counter

class Weights:
    def __init__(self):
        self.w={}

    def clear(self):
        self.w={}

    def plus(self,feats):
        self.zeros(feats)
        self.w.update([(e,self.w[e]+c) for e,c in feats])

    def minus(self,feats):
        self.zeros(feats)
        self.w.update([(e,self.w[e]-c) for e,c in feats])

    def val(self,feats):
        self.zeros(feats)
        return sum([self.w[e]*c for e,c in feats])

    def normalize(self,norm):
        for e,c in self.w.iteritems():
            self.w[e]=self.w[e]/norm.w[e]

    def zeros(self,feats):
        self.w.update([(e,0.5) for e,c in feats if not self.w.has_key(e)])

        
    def weights(self):
        return self.w.items()


