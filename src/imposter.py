#!/usr/bin/env python
# -*- coding: utf-8
# 
# Example of Usage : 
# If we want to generate 15 imposters of spanish language , we use the next command 
# python src/imposters_generator.py --lang sp --seed training/ --output esimposters --imposters 15 
#
# If we want to generate 150 imposters of spanish language , we use the next command 
# python src/imposters_generator.py --lang en --seed training/ --output enimposters --imposters 150
#

import os,re, sys, glob, codecs, requests, getopt, justext , shutil, time
import numpy as np
from BeautifulSoup import BeautifulSoup

#
# Variable
# --------
# lang
# Dictionary with the definition of every available language.
# 
# Skeleton
# --------
# langsearch (string):
#	Equivalent of the language in Google search.
#
# min (int),  max(int):
#	Range to qualify the length of the corpus. This variable must be setted for every language to get a best approximation 
#	If the length < min then good corpus. If the length between min and max, or length > max then good corpus
#
# lang (string):
#	Name of the language, used to get the stop word list
#
lang = {
	'ES': {'imposters': 1500,'langsearch':'es', 'min' : 50, 'max':70, 'lang':'Spanish'},
	'EN': {'imposters': 1200,'langsearch':'en', 'min' : 50, 'max':80, 'lang':'English'},
	'GR': {'imposters': 1300,'langsearch':'el', 'min' : 50, 'max':90, 'lang':'Greek'},
	'NL': {'imposters': 1100,'langsearch':'nl', 'min' : 60, 'max':70, 'lang':'Dutch'},
}

#
# Function
# --------
# getCorpus
# Get the corpus from a HTML text using justext python's library. 
#
# Parameters
# ----------
# html (string) :
#	HTML text
# 
# stopwords (list) :
#	List of stop words, used by justext to get a good qualification of the clean text
#
# lmin (int), lmax (int) : 
# 	Range to qualify the lenght of the corpus.	
#
# Returns
# -------
# full_text (string):
#	The clean corpus of a web page
#

def getCorpus(html, stopwords, lmin, lmax):	
	full_text = []
	paragraphs = justext.justext(html, stopwords, lmin, lmax) 
	for paragraph in paragraphs:
		if paragraph.cf_class == 'good':
			real_text = ''.join("%s" % i.encode('utf-8') for i in paragraph.text_nodes)
			full_text.append(real_text)			
	return ' '.join(full_text)

#
# Function
# --------
# doSearch
# Function to do a search in Google to get the first ten result of a query. 
# The ten links are processed to get the corpus of the sites and are saved as imposter's documet.
# BeautifulSoup is used here ;)
#
# Parameters
# ----------
# query (string) :
#       The text to search in Google. Example 'romeo visita México', 'apple green market'
# 
# selection (list) :
#	List with the selected language (variable lang), all the properties are saved in this variable
#
# stopwords (list) : 
#       List of stop words, used by justext to get a good qualification of the clean text
#
# path (string) : 
#	Path where the file is saved
#

def doSearch(query, selection, stopwords, path):	
	print "Generated query : %s " % query
	search = 'https://www.google.com/search?q=%s&lr=lang_%s' % (query, selection['langsearch'])
	
	try:
		r = requests.get(search,timeout=5, verify = False )
		bs = BeautifulSoup(r.text)

		for result in bs.findAll('h3','r'):
			a = result.find('a')
			href =re.split(r'\/(.*)\?q=(.*)\&sa',a.get('href'))

			try :	
				#We verify if the link is an url and it is not a file	
				if href[1] == 'url' and any( href[2].upper().endswith(ext) for ext in ('.XLS','.XLSX','.PDF','.DOC')) == False :

					source = requests.get(href[2],timeout=5)
					corpus = getCorpus(source.text, stopwords, selection['min'], selection['max'])

					if corpus : 
						size = len(glob.glob(path+"/*.txt")) + 1
						number = "%04d"% size
	
						print "Creating imposter : %s - %s" % (number,href[2])
						imposter = open(path+"/imposter"+number+".txt","w")
						imposter.write(corpus)
						imposter.close()
			except:
				isfile = 1
	except:
		time.sleep(1)
		print "Error"
		#doSearch(query,selection,stopwords,path)


#
# Function
# --------
# doImposter
# Function that generates the imposter's documents.
# In first place we find all the documents of the language related. It's important use the structure of PAN competition. 
# If we select Spanish (SP) , the function will try to find all the .TXT files in the SP directories
# 
# Parameters
# ----------
# seed (string) :
#	The path of the directory where the .TXT files to process are located
# 
# out (string) :
#	Name of the directory that will be created
#
# mainlang (string):
#	Language to be processed, this option is determinated by the nomenclature used by PAN. SP = Spanish, EN = English, etc.
# 
# imposters(int) : 
#	Number of impostors that has to be created
#

def doImposter(seed,out,mainlang,imposters):
	
	# We find all the TXT of the LANG directory 
	# /PATH/LANG/*.TXT
	#path    = seed+mainlang+"*/*.txt"

	path = seed+"/*.txt"
	files = glob.glob(path)

	# Numbers of files to be chosen. This file are mixed to get random words
	file_choice = 3
	# Number of words to be chosen to build the query.
	word_choice = 3

	words   = []
	selection = lang[mainlang]

	# Random selection of the files to be mixed
	randomfiles = np.random.choice(files, file_choice)

	for single_file in randomfiles:
		textwords = ''.join( [line.strip() for line in codecs.open(single_file,'r','utf-8')] ).split()
		words = words + textwords

	stopwords =  justext.get_stoplist(selection['lang'])
	
	# After choose a text, we elimiate all the stop words of the variable
	cleanwords = [word for word in words if word not in set(stopwords)]	

	# Creation of ouput directory
	# output = os.path.join(out,mainlang)
	output = out 
	if not os.path.exists(output):
		os.makedirs(output)
	# ERASE 
	#else: 
	#	shutil.rmtree(out)
	#	os.makedirs(output)		
		

	created = 0
	print "Max imposters : %s" % imposters
	while created <= int(imposters) :
        	query = ' '.join( np.random.choice( cleanwords, word_choice) )
		try:
			doSearch(query, selection, stopwords, output)
		except:
			print "Error"
		created = len(glob.glob(output+"/*.txt"))

def main(argv):
	mainlang = ""
	seed = ""
	out  = ""
	imp  = 0
	
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["lang=","seed=","output=","imposters="])
	except getopt.GetoptError:
		print "Usage : imposter.py --lang [ES|EN|GR|NL]--seed <directory> --output <directory> --imposters <number>"
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print "imposter.py --lang [ES|EN|GR|NL] --seed <directory> --output <directory> --imposters <number>"
			sys.exit()
		elif opt in("--l","--lang"):
			mainlang = arg
		elif opt in("--s","--seed"):
			seed = arg
		elif opt in("--o","--output"):
			out  = arg
		elif opt in("--i","--imposters"):
			imp  = arg
	
	try:
		doImposter(seed,out,mainlang.upper(), imp)	
	except :
		print "Bad parameters"
if __name__ == "__main__":
	main(sys.argv[1:])

