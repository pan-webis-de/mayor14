#!/usr/bin/env python
# -*- coding: utf-8
# 
import random,glob, sys,os, getopt
import docread as dr
import numpy as np

lang = {
	'SP': {'percent': 0.40},
	'EN': {'percent': 0.35},
	'GR': {'percent': 0.30},
}


def langPercent(name):
	return lang[name[:2]]['percent']

def getSample(path):
	print path
	problems = dr.problems(dr.dirproblems(path,r".*\.txt"))

	for dirname, (files,unknow) in problems:

		percent = langPercent(dirname)
		print percent
		docs = ""
		for file in files:
			docs = docs + file[1]
		count = dr.bow(docs)	
		tup = [x for x in  sorted(count[0].iteritems() , key=lambda tup:tup[1],reverse = True)]

		sample = int(round(float(len(tup))*float(percent)))
	
def main(argv):
	seed = ""
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["seed="])
	except:
		sys.exit(2)

	for opt,arg in opts:
		if opt in("--s","--seed"):
			seed = arg	

	try:
		getSample(seed)
	except:
		print "Bad parameters"

if __name__ == "__main__":
	main(sys.argv[1:])

