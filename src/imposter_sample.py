#!/usr/bin/env python
# -*- coding: utf-8

import random,os,getopt, sys, glob 
import docread as dr
import imposter
import create_sample as sample
import distance
import time

dbylang = {
        'EN' : {'method' : distance.jacard2, 'impostersample' : 230 , 'times' : 10, 'corpuspercent' : 0.75 , 'score' : 0.63 },
        'GR' : {'method' : distance.jacard2, 'impostersample' : 300 , 'times' : 20, 'corpuspercent' : 0.70 , 'score' : 0.63 },
        'NL' : {'method' : distance.jacard2, 'impostersample' : 330 , 'times' : 15, 'corpuspercent' : 0.50 , 'score' : 0.64 },
	'ES' : {'method' : distance.jacard2, 'impostersample' : 450 , 'times' : 1,  'corpuspercent' : 0.70, 'score' : 0.5 },
}

directories_bygenre = {
	'ENNOVELS'    	: 'EN',
	'ENESSAYS'    	: 'EE',
	'NLESSAYS'    	: 'DE',
	'NLREVIEWS'  	: 'DR',
	'GRNEWS'	: 'GR',
	'ESNEWS' 	: 'SP',
}

directories_bylang = {
	'ES'		: 'S',
	'GR'		: 'G',
	'NL'		: 'D',
	'EN'		: 'E',
}
langofdirectory = {
	'EN'		: 'EN',
	'EE'		: 'EN',
	'DE'		: 'NL',
	'DR'		: 'NL',
	'GR'		: 'GR',
	'SP'		: 'ES',
}


def getLang (directory):
	return langofdirectory[directory]

def getOptions(lang):
	opt = {
		'method' 	: dbylang[lang]['method'],
		'times'		: dbylang[lang]['times'],
		'score'		: dbylang[lang]['score'],
		'percentlang'	: dbylang[lang]['corpuspercent'],
		'imp_sample'	: dbylang[lang]['impostersample'],	 
	}
	return opt


def changeOptions(opts, otheropts):
	for k in otheropts.keys():
		opts[k] = otheropts[k]
	return opts

def getImposterSample(lang, seed, genre, imposters, uOptions, doImposter):
	start = time.clock()	
	allproblems = os.listdir(seed)
	
	if lang !="":
		if genre != "":	
			startlang = directories_bygenre[lang+genre]
		else:
			startlang = directories_bylang[lang]

		attackproblems = [d for d in allproblems if d.startswith(startlang)]
	else:
		attackproblems = allproblems

	if doImposter == True :
		if lang!= "":
			num_imposters = imposter.lang[lang]['imposters']

		for problem in sorted(attackproblems):
			current_problem = seed+problem
                	imposters_problem = os.path.join(imposters,problem)
                	imposter.doImposter( current_problem, imposters_problem , lang, num_imposters)
	
	if lang!="" :	
		opts = getOptions(lang)
		if uOptions != False :
			opts = changeOptions(opts,uOptions)

	results = []

	f = open('answers_imposters.txt','w')

	global_problems = sample.getFiles(seed)
	
	for problem in sorted(attackproblems):		
		current_problem   = seed+problem
		imposters_problem = os.path.join(imposters,problem)

		file_problems = sample.processFile( global_problems , problem)
		imposters_files = os.listdir(imposters_problem)

		score = 0
		
		if lang == "":
			l = getLang(problem[0:2])
			opts = getOptions(l)
			if uOptions != False:
				opts = changeOptions(opts,uOptions)
		
		for K in range(0, opts['times']):
			id_words = sample.getIdsToSample( file_problems["merged"] , lang , opts['percentlang'])

			known_file = random.sample( file_problems["known"] , 1)[0]

                	known_sample  = sample.getFromText( id_words, known_file )
               		unkown_sample = sample.getFromText( id_words, file_problems["unknown"] ) 

			random_imposters_files = random.sample(imposters_files, opts['imp_sample'])
			
			_method = opts['method']

			for imposter_file in random_imposters_files :
				imposter_sample = sample.getFromFile( id_words,  os.path.join(imposters_problem,imposter_file) )
	
				dk_di = _method(known_sample, imposter_sample)
				dk_du = _method(known_sample, unkown_sample)
				du_di = _method(unkown_sample, imposter_sample)
				du_dk = _method(unkown_sample, known_sample)

				if  dk_du * du_dk >  dk_di * du_di :
					score += 1/ float( (opts['times']) * len(random_imposters_files) ) 

		result = "N"
		if ( score > opts['score']):
			result = "Y"

		strToPrint = "%s %s %f" %  (problem, result,score)
		strToFile = "%s %f " % (problem, score)
		f.write(strToFile+"\n")
		print strToPrint
	return 0

def main(argv):

	mainlang 	= ""
	seed 		= ""
	genre 		= ""
	imposters 	="imposters"
	output 		= "output"
	doImposters 	= False
	externalOptions = False
	sample 		= ""
	times 		= ""
	corpus 		= ""
	score 		= ""
	
	try:
		opts, args = getopt.getopt(argv, "hi:o:",["lang=","seed=","genre=","output=","imposters=","doimposters=","is=","rp=","co=","sc="])
	except getopt.GetoptError:
		print "Usage"

	for opt, arg in opts:
                if opt == '-h':
                        print "imposter.py --lang [NL|EN|GR|ES] --seed <directory> --genre=[ESSAYS|REVIEWS|NOVELS|NEWS] --output <directory> --imposters <directory> --doimposters=[TRUE|FALSE]"
                        sys.exit()
                elif opt in("--lang"):
                        mainlang = arg.upper()
                elif opt in("--seed"):
                        seed = arg
		elif opt in("--genre"):
			genre = arg.upper()
                elif opt in("--output"):
                        output  = arg
                elif opt in("--imposters"):
                        imposters  = arg
		elif opt in("--doimposters"):
			doImposters = True
		elif opt in("--is"):
			sample = int(arg)
		elif opt in("--rp"):
			times = int(arg)
		elif opt in("--co"):
			corpus = float(arg)
		elif opt in("--sc"):
			score = float(arg)
	
	if sample!="" and times !="" and corpus !="" and score!="":
		externalOptions = {"imp_sample" : sample , "times": times, "corpuspercent" : corpus , "score": score}

	try:
		getImposterSample(mainlang, seed, genre, imposters, externalOptions,doImposters)			
	except ValueError:
		print "error"

if __name__ == "__main__" :
	try: 
		main(sys.argv[1:])
	except ValueError:
		print "BAD, Try again"

