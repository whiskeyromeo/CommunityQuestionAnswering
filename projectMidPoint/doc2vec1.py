"""
	2nd best performance, worse than implementation
	in doc2vec3.py
"""

from nltk.corpus import stopwords

from gensim import utils
from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument, Doc2Vec

from QuestionFileCreator import QuestionCleaner, getQuestions
from cosineSimilarity import cosineSimilarity
from elementParser import elementParser, originalQuestionParser

from random import shuffle
from pprint import pprint
import csv
import re
import logging
import numpy
import os

from sourceFiles import thisList, origQfilePath

stops = set(stopwords.words('english'))


'''
	Preps the list of TaggedDocs to be fed into Doc2Vec
	Params:
		A list of questions
	Returns:
		A list of tagged documents
'''
def prepLabeledSentList(questions = []):
	mod_questions = []
	# for each of the questions create a TaggedDoc, append to the new list
	for q in questions:
		mod_questions.append(TaggedDocument([i for i in q['question'].lower().split() if i not in stops], (q['id'])))
	return mod_questions


'''
	Memory friendly implementation of Doc2Vec with decreasing learning rate to reduce decay
	Params:
		questions: A list of questions
	Returns:
		model: A doc2vec model
'''
def RareDoc2Vec(questions):
	mod_questions = prepLabeledSentList(questions)
	model = Doc2Vec(alpha=0.025, min_alpha=0.025)  # use fixed learning rate
	model.build_vocab(mod_questions)
	for epoch in range(10):
	    model.train(mod_questions)
	    model.alpha -= 0.002  # decrease the learning rate
	    model.min_alpha = model.alpha  # fix the learning rate, no decay
	# save the model for future use
	model.save('./tmp/RareModel')
	return model


'''
	Sets the doc2vec vectors for each of the questions
	Params:
		hashmap: An list containing hashes with questions and properties
		model: A doc2vec model
'''
def setVectors(hashmap, model):
	for q in hashmap:
		q['D2V_qVec1'] = model.infer_vector(q['question'])


'''
	Modifies the hashmap to incorporate the doc2vec output for each question
	Params:
		hashmap: An list containing hashes with questions and properties
	Returns:
		model: A doc2vec model
'''
def BuildDoc2VecMap(hashmap):
	# get the mini hash map of questions and ids
	questions = getQuestions(hashmap)
	# clean the questions, removing punctuation and whitespace
	questions = QuestionCleaner(questions)
	# Create the Doc2Vec Model
	model = RareDoc2Vec(questions)
	# Set the vectors back in the hashmap
	setVectors(hashmap, model)
	return model


model = BuildDoc2VecMap(thisList)

"""
	Create a prediction file
	Arguments:
		filePath : Should be a filepath which conforms to the structure needed for the originalQuestionParser
		questionList : Should be a list of hashes containing the information about the provided questions
	Output:
		file: takes the filename from the filePath and saves a .pred file based on that name
		containing the information needed to run the MAP against it 
"""
def createPredictionFile(filePath, model, withStops=True):
	#pull the test questions out from the filePath
	testQuestions = originalQuestionParser(filePath)
	# Get the name of the directory and split the filename off
	head, tail = os.path.split(filePath)
	tail = tail.split('.')[0]
	# Save the file according to whether stopwords are removed before processing
	if(withStops):
		predFile = tail + '-d2v-with-stops.pred'
	else:
		predFile = tail + '-d2v.pred'
	# prepare to write the file
	with open(predFile, "w") as tsvfile:
		writer = csv.writer(tsvfile, delimiter="\t")
		# iterate through the test questions, getting the vector
		for t_question in testQuestions:
			if(withStops):
				t_question['D2V_OVec1'] = model.infer_vector(t_question['origQuestion'])
			else: 
				t_question['origQNoStops'] = " ".join([i for i in t_question['origQuestion'].lower().split() if i not in stops])
				t_question['D2V_OVec1'] = model.infer_vector(t_question['origQNoStops'])

			vecList = []
			# iterate through each question set associated with each test questions
			for rel_quest in t_question['rel_questions']:
				# and set the vectors
				if(withStops):
					rel_quest['D2V_qVec1'] = model.infer_vector(rel_quest['question'])
				else:
					rel_quest['relQNoStops'] = " ".join([i for i in rel_quest['question'].lower().split() if i not in stops])
					rel_quest['D2V_qVec1'] = model.infer_vector(rel_quest['relQNoStops'])
				vecList.append(rel_quest['D2V_qVec1'])		
			# generate the cosineSimilarity against the test question
			simMatrix = cosineSimilarity(t_question['D2V_OVec1'], vecList)
			for idx, row in enumerate(t_question['rel_questions']):
				row['simVal'] = simMatrix[idx]
				# write the obtained similarity values to the prediction file
				writer.writerow([t_question['quest_ID'], row['rel_quest_ID'], 0, row['simVal'], row['relevant']])
				

#Call the function to create the prediction files
createPredictionFile(origQfilePath, model, False)
createPredictionFile(origQfilePath, model)


