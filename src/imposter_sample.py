#!/usr/bin/env python
# -*- coding: utf-8

import random,os,getopt, sys, glob 
import docread as dr
import imposter
import create_sample as sample
import distance

dbylang = {
	'SP' :  {'impostersample': 300,'method' : distance.jacard2 , 'times' : 80 } 
}

def getImposterSample(lang, seed,genre,imposters, output, doImposter):
	
	num_imposters = imposter.lang[lang]['imposters']

	allproblems = os.listdir(seed)
	
	if(lang !="") :
		attackproblems = [d for d in allproblems if d.startswith(lang)]
	else:
		attackproblems = allproblems

	if doImposter == True :
		for problem in attackproblems:
			current_problem = seed+problem
                	imposters_problem = os.path.join(imposters,problem)
                	imposter.doImposter( current_problem, imposters_problem , lang, num_imposters)


	#attackproblems = ['SP100','SP002','SP001','SP007']
	#attackproblems = ['SP100']

	for problem in sorted(attackproblems):
		current_problem =   seed+problem
		imposters_problem = os.path.join(imposters,problem)
		print "Solving : " + current_problem
		#print "Imposters : "+ imposters_problem
		
		file_problems = sample.mergeKnows(seed)	
		
		method = dbylang[lang]['method']
		times  = dbylang[lang]['times']	
               	imposters_sample = dbylang[lang]['impostersample']

		imposters_files = os.listdir(imposters_problem)

		#for k in range(1, times):
		#id_words = sample.getIdsToSample( file_problems["known"] , lang) 
		#imposters_files = os.listdir(imposters_problem)

		#known_sample = sample.getFromText( id_words, file_problems["known"] )
		#unkown_sample = sample.getFromText( id_words , file_problems["unknown"] ) 

		score = 0
		for K in range(1, times):
			id_words = sample.getIdsToSample( file_problems["known"] , lang) 
                	imposters_files = os.listdir(imposters_problem)

                	known_sample = sample.getFromText( id_words, file_problems["known"] )
               		unkown_sample = sample.getFromText( id_words , file_problems["unknown"] ) 

			random_imposters_files = random.sample(imposters_files, imposters_sample)
			for imposter_file in random_imposters_files :
				imposter_sample = sample.getFromFile( id_words,  os.path.join(imposters_problem,imposter_file) )
	
				#print "DK_DI"	
				dk_di = method(known_sample, imposter_sample)

				#print "DK_DU"
				dk_du = method(known_sample, unkown_sample)
			
				#print "DU_DI"
				du_di = method(unkown_sample, imposter_sample)
				#print "DU_DK"
				du_dk = method(unkown_sample, known_sample)			
			
				#print "imposter %s " % imposter_file	
				#print "DK - DU %s " % dk_du 
				#print "DU - DK %s " % du_dk
				#print "DK_DU* DU_DK %f" % (dk_du*du_dk) 
				#print "DK - DI %s " % dk_di
				#print "DU - DI %s " % du_di	
				#print "DK_DI * DU_DI %f " % (du_di*dk_di)
				if  dk_du * du_dk >  dk_di * du_di :
					score += 1/ float( (times-1))
					#score += 1/ float( len(imposters_files[:1]) )
					#score += 1/ float( (times-1) * len(imposters_files) ) 


		#print len(imposters_files)	
		print "Score %s" % score
		result = "N"
		if ( score > 0.5):
			result = '\033[92m'+"Y"+'\033[0m'
		print "Result %s " % result

def main(argv):

	mainlang = ""
	seed = ""
	genre = ""
	imposters ="imposters"
	output = "output"
	doImposters = False
	
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
		getImposterSample(mainlang, seed, genre, imposters, output, doImposters)			
	except ValueError:
		print ValueError

if __name__ == "__main__" : 
	main(sys.argv[1:]) 
		

