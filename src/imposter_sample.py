#!/usr/bin/env python
# -*- coding: utf-8

import os,getopt, sys, glob 
import docread as dr
import imposter


def getImposterSample(lang, seed,genre,imposters, output):
	
	num_imposters = imposter.lang[lang]['imposters']

	allproblems = os.listdir(seed)
	
	if(lang !="") :
		attackproblems = [d for d in allproblems if d.startswith(lang)]
	else:
		attackproblems = allproblems

	for problem in attackproblems:
		current_problem = seed+problem
		print "Solving : " + current_problem
		print "Imposters : "+ imposters+"/"+problem
		imposter.doImposter( seed+problem, os.path.join(imposters,problem), lang, num_imposters)	
			
	

def main(argv):

	mainlang = ""
	seed = ""
	genre = ""
	imposters ="imposters"
	output = "output"

	try:
		opts, args = getopt.getopt(argv, "hi:o:",["lang=","seed=","genre=","output=","imposters="])
	except getopt.GetoptError:
		print "Usage"

	for opt, arg in opts:
                if opt == '-h':
                        print "imposter.py --lang [DU|EN|GR|SP] --seed <directory> --genre=[ESSAYS|REVIEWS|NOVELS|NEWSPAPER] --output <directory> --imposters <directory>"
                        sys.exit()
                elif opt in("--l","--lang"):
                        mainlang = arg
                elif opt in("--s","--seed"):
                        seed = arg
		elif opt in("--g","--genre"):
			genre = arg
                elif opt in("--o","--output"):
                        output  = arg
                elif opt in("--i","--imposters"):
                        imposters  = arg
	
	try:
		getImposterSample(mainlang, seed, genre, imposters, output)			
	except ValueError:
		print ValueError

if __name__ == "__main__" : 
	main(sys.argv[1:]) 
		

