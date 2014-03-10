#!/usr/bin/env python
# -*- coding: utf-8

import os,getopt, sys, glob 
import docread as dr
import imposter
import create_sample as sample
import distance

dbylang = {
	'SP' :  distance.jacard2
}

def getImposterSample(lang, seed,genre,imposters, output):
	
	num_imposters = imposter.lang[lang]['imposters']

	allproblems = os.listdir(seed)
	
	if(lang !="") :
		attackproblems = [d for d in allproblems if d.startswith(lang)]
	else:
		attackproblems = allproblems

	for problem in attackproblems:
		current_problem =   seed+problem
		imposters_problem = os.path.join(imposters,problem)
		print "Solving : " + current_problem
		print "Imposters : "+ imposters_problem
		
		#DO IMPOSTERS
		imposter.doImposter( current_problem, imposters_problem , lang, num_imposters)	

		file_problems = sample.mergeKnows(seed)	
		id_words = sample.getIdsToSample( file_problems["known"] , lang) 
		
		imposters_files = os.listdir(imposters_problem)

		known_sample = sample.getFromText( id_words, file_problems["known"] )

		unkown_sample = sample.getFromText( id_words , file_problems["unknown"] ) 

		method = dbylang[lang] 
		score = 0	
		for imposter_file in imposters_files :
			imposter_sample = sample.getFromFile( id_words,  os.path.join(imposters_problem,imposter_file) )
		
			dk_di = method(known_sample, imposter_sample)
			dk_du = method(known_sample, unkown_sample)
			
			du_di = method(unkown_sample, imposter_sample)
			du_dk = method(unkown_sample, known_sample)			
			#print "imposter %s " % imposter_file	
			#print "DK - DU %s " % dk_du 
			#print "DU - DK %s " % du_dk
			#print "DK - DI %s " % dk_di
			#print "DU - DI %s " % du_di	
			if  dk_du * du_dk < dk_di * du_di :
				score += 1/float(len(imposters_files))

		#print len(imposters_files)	
		print score


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
		

