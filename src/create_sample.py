#!/usr/bin/env python
# -*- coding: utf-8
# 
import random,glob, sys,os, getopt
import docread as dr
import numpy as np

lang = {
	'SP': {'percent': 0.40},
	'EN': {'percent': 0.50},
	'GR': {'percent': 0.30},
}

def langPercent(name):
	return lang[name[:2]]['percent']


def getSelection(counter, selection):
	return {element : counter[element] for element in selection }

def getSample(path):
	problems = dr.problems(dr.dirproblems(path,r".*\.txt"))
	
	data = {}
	for dirname, (files,unknow) in problems:
		data[dirname]={}
		percent = langPercent(dirname)
		docs = ""
		for file in files:
			docs = docs + file[1]

		count = dr.bow(docs)	
		
		sample = int(round(float(len(count[0]))*float(percent)))  
		selection= random.sample(count[0],sample)
	
		data[dirname]['total'] = getSelection(count[0],selection)

		for file in files:
			namefile = file[0].split("/")[-1]
			count_file = dr.bow(file[1])
			data[dirname][namefile] = getSelection(count_file[0],selection)
		
	return  data
	
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
	except ValueError:
		print ValueError

if __name__ == "__main__":
	main(sys.argv[1:])

