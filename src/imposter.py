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
import os,re, sys, glob, codecs, requests, getopt, justext , shutil, time, ssl, json, string
import numpy as np
from collections import Counter
from os import walk
from pprint import pprint
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
	'spanish': {'imposters': 1500,'langsearch':'es', 'min' : 50, 'max': 300, 'lang':'Spanish'},
	'english': {'imposters': 1200,'langsearch':'en', 'min' : 50, 'max': 300, 'lang':'English'},
	'greek'	 : {'imposters': 1300,'langsearch':'el', 'min' : 50, 'max': 240, 'lang':'Greek'},
	'dutch'	 : {'imposters': 1100,'langsearch':'nl', 'min' : 50, 'max': 200, 'lang':'Dutch'},
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
def getCorpus(html, language, lmin, lmax):	
	full_text = ""
	try:
		paragraphs = justext.justext(html, justext.get_stoplist( language ),lmin, lmax) 
		for paragraph in paragraphs:
			# print paragraph.cf_class
			# real_text = ''.join("%s" % i.encode('utf-8') for i in paragraph.text_nodes)
			# print real_text
			# print "\n"
			if paragraph.cf_class =='good':
				real_text = ''.join("%s" % i.encode('utf-8') for i in paragraph.text_nodes)
				full_text = full_text + real_text
		
		# print full_text
		complete_text = full_text.split(" ")[:1500]
		# print "Words: %s" % ( len(complete_text) )
		if len(complete_text) > 500:
			return ' '.join(complete_text)
	except IOError as e:
		print "Time Sleep I/O error({0}): {1}".format(e.errno, e.strerror)
	return None
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
def doSearch(language, query, stopwords, path):	
	print "Generated query : %s " % query
	search = 'https://www.google.com/search?q=%s&lr=lang_%s' % (query+" -filetype:pdf", lang[language]['langsearch'] )
	imposters_created = 0
	try:
		r = requests.get(search,timeout=5, verify = False )
		bs = BeautifulSoup(r.text)

		for result in bs.findAll('h3','r'):
			a = result.find('a')
			href =re.split(r'\/(.*)\?q=(.*)\&sa',a.get('href'))

			try :	
				if len(href) > 1 : 
					#We verify if the link is an url and it is not a file	
					if href[1] == 'url' and any( href[2].upper().endswith(ext) for ext in ('.XLS','.XLSX','.PDF','.DOC')) == False :
						try:
							source = requests.get(href[2],timeout=3)
							corpus = getCorpus(source.text, lang[language]['lang'], lang[language]['min'], lang[language]['max'])
							if corpus : 
								size = len(glob.glob(path+"/*.txt")) + 1
								number = "%04d"% size
								print "Creating imposter : %s - %s" % (number,href[2])
								imposter = open(path+"/imposter"+number+".txt","w")
								imposter.write(corpus)
								imposter.close()
								imposters_created+=1
							else:
								print "Insufficient corpus: %s" % (href[2])
						except:
								isfile = 1
			except IOError as e:
				isfile = 1
				print "I/O error({0}): {1} {2}".format(e.errno, e.strerror, href[2])
	except IOError as e:
		time.sleep(1)
		print "Time Sleep I/O error({0}): {1}".format(e.errno, e.strerror)
	return imposters_created
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
def doImposter(seed, out, imposters ):
	# We find all the TXT of the LANG directory 
	# /PATH/LANG/*.TXT
	#path    = seed+mainlang+"*/*.txt"
	imposters_limit = 10
	attempts = 50

	path = seed+"/contents.json"
	content = open(path)
	data = json.load(content)
	
	genre    = data['genre']
	language = data['language']

	stopwords_path = "data/stopwords_"+language+".txt"
	stopwords = [line.strip() for line in  codecs.open(stopwords_path,'r','utf-8')]

	problems = data['problems']
	limit_search = 5

	output = out+"/"+language+"_"+genre
	if not os.path.exists(output):
		os.makedirs(output)

	remove_punctuation_map = dict((ord(char), None) for char in ( string.punctuation + "+”¿?-.“") )

	for problem in problems:
		print "\nAnalizing "+problem + ":\n"
		
		known_files = glob.glob( seed+"/"+problem+"/know*.txt")
		words = []
		for single_file in known_files:
			textwords = ''.join( [line.translate(remove_punctuation_map).strip() for line in codecs.open(single_file,'r','utf-8')] ).split()
			most_used =  Counter(x for x in textwords if x not in stopwords).most_common(10)
			words_to_search = []
			for elemen, count in most_used:
				words_to_search.append(elemen)
			# words_to_search = set(textwords)-set(stopwords)
			
			created = 0
			attempt = 0
			while created < imposters_limit and attempt < attempts :
				query = ' '.join( np.random.choice( (words_to_search), limit_search) )
				created += doSearch(language, query, stopwords, output)
				attempt += 1
				print "Creados %s " % (created)
			
def main(argv):
	mainlang = ""
	seed = ""
	out  = ""
	imp  = 1000
	# stopwords_path = "data/stopwords.txt"

	try:
		opts, args = getopt.getopt(argv,"hi:o:",["seed=","output="])
	except getopt.GetoptError:
		print "Usage : imposter.py --seed <directory> --output <directory> --imposters <number>"
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print "imposter.py --seed <directory> --output <directory> --stopwords <path>"
			sys.exit()
		elif opt in("--s","--seed"):
			seed = arg
		elif opt in("--o","--output"):
			out  = arg
		elif opt in("--st","--stopwords"):
			stopwords_path  = arg
	
	try:
		# stopwords = [line.strip() for line in  codecs.open(stopwords_path,'r','utf-8')]
		for (dirpath, dirnames, filenames) in walk(seed):
			for dirname in dirnames:
				doImposter( seed + "/" + dirname , out, imp );
			break

	except ValueError:
		print "Bad parameters"
if __name__ == "__main__":
	main(sys.argv[1:])