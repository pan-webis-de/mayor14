#!/usr/bin/env python
# -*- coding: utf-8
# 
# Example of usage : 
# The main function to get all the documents of a directory the next structure 
# {'DIRNAME' : {'total' : {WORD COUNTS} , 'FILENAME' : {WORD COUNTS}} }
#
# {'EN04' : {'total: {'worda':4,'wordb':2,'wordc':3}, 'know01.txt': {'worda':2} ,'unknow.txt' : {'wordc':1} } }
#

import math,random,glob, sys,os, getopt
import docread as dr
import numpy as np


#
# Variable
# --------
# lang
# Dictionary with the percentage of search for every language
# 
# Skeleton
# --------
# percent (float):
#	Percent of search
#
lang = {
	'SP': {'percent': 0.40},
	'EN': {'percent': 0.01},
	'GR': {'percent': 0.30},
	'DE': {'percent': 0.80},
	'DR': {'percent': 0.70},
	'EE': {'percent': 0.30},
}

#
# Function
# --------
# langPercent
# Function to get the language of a directory and get the percent of the language
#
# Parameters
# ----------
# directory (string):
#	Name of the directory , example : ES001 , EN001
def langPercent(directory):
	return lang[directory[:2]]['percent']

#
# Function
# -------
# getSelection 
# Function to get the same elements of two different list
#
# Parameters 
# ----------
# 
# counter (list)
#	Count list example {casa : 1 , verde : 3}
# selection (list)
#	Sample of list to be selected
#
def getSelection(counter, selection):
	return {element : counter[element] for element in selection if counter[element] > 0}


def mergeKnows(path):
	problem = dr.problems ( dr.dirproblems ( path) )
	merge_file = ""
	unknown_file = ""

	for dirname , (known,unknown) in problem:
		for file in known:
			merge_file = merge_file + file[1]

		for ufile in unknown: 
			unknown_file = unknown_file + ufile[1]

	return {'known' : merge_file , 'unknown' : unknown_file}

def getIdsToSample(text, selected_lang):
	percent = lang[selected_lang]['percent']
	count = dr.bow(text)
	sample = int( math.ceil( len( count[0] ) * percent ) )
	selection = random.sample(count[0] , sample)
	return selection

def getFromText( idwords, text):
	count_file = dr.bow( text)
	return getSelection( count_file[0] , idwords)

def getFromFile( idwords, path):
	count_file = dr.bow ( dr.readdoc(path) )
	return getSelection( count_file[0] , idwords)

#
# Function
# --------
# getSample
# Function to get the sample of all the files of directory
# 	First we read all the documents of a directory and are concatenated at one Var : docs
# 	With var "docs" we get the BOW reponse (include in docread.py)
#	BOW response get the count of the words, we get a sample in relation of the percetage of a language , we call this process 'total'
#	With our total, we process every single file and get the same variables as total.
#	The final response is a single list. Example : {'EN04' : {'total: {'worda':4,'wordb':2,'wordc':3}, 'know01.txt': {'worda':2} ,'unknow.txt' : {'wordc':1} } } 
#
# Parameters
# ----------
# path(string)
# Path of the files
#
def getSample(path):
	#problems = dr.problems(dr.dirproblems(path,r".*\.txt"))
	problems = dr.problems ( dr.dirproblems ( path ) )
	data = {}
	for dirname, (files,unknow) in problems:
		data[dirname]={}
		percent = langPercent(dirname)
		docs = ""
		for file in files:
			docs = docs + file[1]

		count = dr.bow(docs)	
	
		#Sample : Number of words to be obtained based on a percentage of the language	
		sample = int(round(float(len(count[0]))*float(percent)))  
		#Sample of words of all the total of docs
		selection= random.sample(count[0],sample)
	
		#We select only the selection in the "count list"
		data[dirname]['total'] = getSelection(count[0],selection)

		for file in files:
			namefile = file[0].split("/")[-1]
			count_file = dr.bow(file[1])
			#We geet the same selection as the final, for every single count of the file
			data[dirname][namefile] = getSelection(count_file[0],selection)
	
	print data	
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

