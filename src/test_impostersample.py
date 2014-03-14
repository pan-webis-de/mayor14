#!/usr/bin/env python
# -*- coding: utf-8

import random , sys

from time import sleep

import imposter_sample as imsa
import distance

import numpy as np

import pymongo
from pymongo import MongoClient

client = MongoClient('localhost',27017)
db = client.authorid

impostersample = range(200,240,10)
times =  range(5,40,5)
corpuspercent = np.arange(0.5,1,0.1)
score = np.arange(0.60,0.80,0.01)

print times
print impostersample
print corpuspercent
print score

lang = 'SP' 
seed = 'data/pan14mini/'
genre = ''
imposters = 'data/resultsmini'


def doThr():
	i = np.random.choice( impostersample	, 1)[0]
	t = np.random.choice( times		, 1)[0]
	c = np.random.choice( corpuspercent	, 1)[0]
	s = np.random.choice( score		, 1)[0]
	
	opt ={
		'SP' : {'methodname': 'jacard2','method' : distance.jacard2, 'impostersample' :  i  , 'times' : t, 'corpuspercent' : round(c,2) , 'score' : round(s,2) }
	}
	print opt
	r = imsa.getImposterSample(lang, seed, genre, imposters, False, opt)
	db.experiment.insert(r)	


for k in range(1,1000):
	doThr()


