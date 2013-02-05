import nltk

def masi_distance (label1, label2):
	return 1 - float(len(label1.intersection(label2)))/float(max(len(label1),len(label2)))
	
