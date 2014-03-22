#!/usr/bin/env python
# -*- coding: utf-8

import random,os,getopt, sys, glob 
import docread as dr
import imposter
import create_sample as sample
import distance
import time

#import pymongo
#from pymongo import MongoClient
#client = MongoClient('localhost',27017)
#db = client.authorid

dbylang = {
	'SP' : {'methodname': 'jacard2','method' : distance.jacard2, 'impostersample' : 230 , 'times' : 5, 'corpuspercent' : 0.60 , 'score' : 0.63 }
}

def getImposterSample(lang, seed,genre,imposters, doImposter , externalOpts):
	start = time.clock()	
	num_imposters = imposter.lang[lang]['imposters']

	allproblems = os.listdir(seed)
	
	if(lang !="") :
		attackproblems = [d for d in allproblems if d.startswith(lang)]
	else:
		attackproblems = allproblems

	if doImposter == True :
		for problem in sorted(attackproblems):
			current_problem = seed+problem
                	imposters_problem = os.path.join(imposters,problem)
                	imposter.doImposter( current_problem, imposters_problem , lang, num_imposters)
	opts = dbylang
	if externalOpts != False: 	
		opts = externalOpts
	 
	method           = opts[lang]['method']
	methodname       = opts[lang]['methodname']
	times            = opts[lang]['times']
	matchscore       = opts[lang]['score']
	percentlang      = opts[lang]['corpuspercent']
	imposters_sample = opts[lang]['impostersample']

	results = []

	for problem in sorted(attackproblems):

		current_problem   =   seed+problem
		imposters_problem = os.path.join(imposters,problem)
		
		print "Solving : " + current_problem		
		
		file_problems = sample.getFiles(seed)	
		imposters_files = os.listdir(imposters_problem)

		score = 0
		for K in range(1, times):
			id_words = sample.getIdsToSample( file_problems["merged"] , lang , percentlang) 
                	imposters_files = os.listdir(imposters_problem)
			
			known_file = random.sample( file_problems["known"] , 1)[0]

                	known_sample  = sample.getFromText( id_words, known_file )
               		unkown_sample = sample.getFromText( id_words, file_problems["unknown"] ) 

			random_imposters_files = random.sample(imposters_files, imposters_sample)

			for imposter_file in random_imposters_files :
				imposter_sample = sample.getFromFile( id_words,  os.path.join(imposters_problem,imposter_file) )
	
				dk_di = method(known_sample, imposter_sample)
				dk_du = method(known_sample, unkown_sample)
				du_di = method(unkown_sample, imposter_sample)
				du_dk = method(unkown_sample, known_sample)			

				if  dk_du * du_dk >  dk_di * du_di :
					score += 1/ float( (times-1) * len(random_imposters_files) ) 


		print "Score %s" % score
		result = "N"
		if ( score > matchscore):
			result = "Y"
		print "Result %s " % result

		obj = {
			"text"  : problem , 
			"score" : score , 
			"result": result
		}
		results.append(obj)
	
	took = time.clock() - start
	experiment = {
		"lang"    	: lang,
		"method" 	: methodname,
		"imposters" 	: imposters_sample,
		"times"		: times,
		"took" 		: took,	
		"score" 	: matchscore,
		"percentcorpus" : percentlang,
		"results" 	: results
	}
	return experiment	
	#db.experiment.insert(experiment)

def main(argv):

	mainlang = ""
	seed = ""
	genre = ""
	imposters ="imposters"
	output = "output"
	doImposters = False
	
	try:
		opts, args = getopt.getopt(argv, "hi:o:",["lang=","seed=","genre=","output=","imposters=","doimposters="])
	except getopt.GetoptError:
		print "Usage"

	for opt, arg in opts:
                if opt == '-h':
                        print "imposter.py --lang [DU|EN|GR|SP] --seed <directory> --genre=[ESSAYS|REVIEWS|NOVELS|NEWSPAPER] --output <directory> --imposters <directory> --doimposters=[TRUE|FALSE]"
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
		elif opt in("--d","--doimposters"):
			doImposters = True
	
	try:
		getImposterSample(mainlang, seed, genre, imposters, doImposters, False)			
	except ValueError:
		print ValueError

if __name__ == "__main__" : 
	main(sys.argv[1:]) 
		

