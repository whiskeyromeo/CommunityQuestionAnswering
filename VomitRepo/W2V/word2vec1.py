from nltk.corpus import stopwords
import gensim
from gensim import utils
from gensim.models import Word2Vec
import numpy as np
from random import shuffle
from pprint import pprint
import csv
import re
import logging
import numpy
import os
import sys
import pickle
import nltk
from pathlib import Path 

from vectorTools import *

sys.path.insert(0, os.path.abspath('..'))
from utils.QuestionFileCreator import QuestionCleaner, getQuestions, getQuestionsFromQTL, getComments, prepModelFolder, initializeLog
from utils.cosineSimilarity import cosineSimilarity
from utils.elementParser import elementParser, originalQuestionParser
from utils.sourceFiles import thisList, origQfilePath
from crawler.jsonDumper import createObjectListFromJson

initializeLog()

def extractWordTokens(questionList):
	tokenList = []
	for q in questionList:
		try: 
			tokenList.append(q['question_tokens'])
		except:
			raise KeyError("question_token not found for record")
	return tokenList
	

def buildBasicW2VModel(questionList):
	tokenList = extractWordTokens(questionList)
	model = Word2Vec(tokenList, size=100, window=5, min_count=3, workers=4)
	return model

# bigram_transformer = gensim.models.Phrases(questionTokens)
# phrase_model = Word2Vec(bigram_transformer[questionTokens], size=100, window=5, min_count=5,workers=4)

# Currently built to take in thisList
# need to reconfigure to make a more general application

qtlQuestions = createObjectListFromJson('../crawler/data/questFileExample.json')
qtlQuestions = getQuestionsFromQTL(qtlQuestions)
QTLMap = buildQuestionMap(qtlQuestions)


questions = getQuestions(thisList)
GenMap = buildQuestionMap(questions)





























# '''
# 	Preps the list of TaggedDocs to be fed into Doc2Vec
# '''
# def prepLabeledSentList(questions = []):
# 	mod_questions = []
# 	# for each of the questions create a TaggedDoc, append to the new list
# 	for q in questions:
# 		mod_questions.append(TaggedDocument([i for i in q['question'].lower().split() if i not in stops], (q['id'])))
# 	return mod_questions


# '''
# 	Memory friendly implementation of Doc2Vec with decreasing learning rate to reduce decay
# '''
# def RareDoc2Vec(questions):
# 	mod_questions = prepLabeledSentList(questions)
# 	model = Doc2Vec(alpha=0.025, min_alpha=0.025)  # use fixed learning rate
# 	model.build_vocab(mod_questions)
# 	for epoch in range(10):
# 	    model.train(mod_questions)
# 	    model.alpha -= 0.002  # decrease the learning rate
# 	    model.min_alpha = model.alpha  # fix the learning rate, no decay
# 	model.save('./tmp/RareModel')
# 	return model


# '''
# 	Sets the doc2vec vectors for each of the questions
# '''
# def setVectors(hashmap, model):
# 	for q in hashmap:
# 		q['D2V_qVec1'] = model.infer_vector(q['question'])


# '''
# 	Modifies the hashmap to incorporate the doc2vec output for each question
# '''
# def BuildDoc2VecMap(hashmap, comments=False):
# 	# get the mini hash map of questions and ids
# 	questions = getQuestions(hashmap)
# 	if(comments):
# 		questions += getComments(hashmap)
# 	# clean the questions, removing punctuation and whitespace
# 	questions = QuestionCleaner(questions)
# 	# Create the Doc2Vec Model
# 	model = RareDoc2Vec(questions)
# 	# Set the vectors back in the hashmap
# 	setVectors(hashmap, model)
# 	return model


# if(Path("tmp/d2v1_model.p").is_file()):
# 	model = pickle.load(open("tmp/d2v1_model.p", "rb"))
# else:
# 	model = BuildDoc2VecMap(thisList)
# 	pickle.dump(model, open("tmp/d2v1_model.p", "wb"))

# """
# 	Create a list of vectors with a 1/1 match for each question in questionList
# """
# def getVectors(questionList):
# 	vecList = []
# 	for vecs in questionList:
# 		vecList.append(vecs["D2V_qVec1"])
# 	return vecList

# """
# 	Create a prediction file
# 	Arguments:
# 		filePath : Should be a filepath which conforms to the structure needed for the originalQuestionParser
# 		questionList : Should be a list of hashes containing the information about the provided questions
# 	Output:
# 		file: takes the filename from the filePath and saves a .pred file based on that name
# 		containing the information needed to run the MAP against it 
# """


# def createW2VPredictionFile(filePath, model, withStops=True):
# 	testQuestions = originalQuestionParser(filePath)
# 	head, tail = os.path.split(filePath)
# 	tail = tail.split('.')[0]
# 	if(withStops):
# 		predFile = tail + '-d2v-with-stops.pred'
# 	else:
# 		predFile = tail + '-d2v.pred'
# 	modelPath = prepModelFolder()
# 	predFile = modelPath + predFile
# 	with open(predFile, "w") as tsvfile:
# 		writer = csv.writer(tsvfile, delimiter="\t")
# 		for t_question in testQuestions:
# 			if(withStops):
# 				t_question['D2V_OVec1'] = model.infer_vector(t_question['origQuestion'])
# 			else: 
# 				t_question['origQNoStops'] = " ".join([i for i in t_question['origQuestion'].lower().split() if i not in stops])
# 				t_question['D2V_OVec1'] = model.infer_vector(t_question['origQNoStops'])

# 			vecList = []
# 			for rel_quest in t_question['rel_questions']:
# 				if(withStops):
# 					rel_quest['D2V_qVec1'] = model.infer_vector(rel_quest['question'])
# 				else:
# 					rel_quest['relQNoStops'] = " ".join([i for i in rel_quest['question'].lower().split() if i not in stops])
# 					rel_quest['D2V_qVec1'] = model.infer_vector(rel_quest['relQNoStops'])
# 				vecList.append(rel_quest['D2V_qVec1'])		
# 			simMatrix = cosineSimilarity(t_question['D2V_OVec1'], vecList)
# 			for idx, row in enumerate(t_question['rel_questions']):
# 				row['simVal'] = simMatrix[idx]
# 				writer.writerow([t_question['quest_ID'], row['rel_quest_ID'], 0, row['simVal'], row['relevant']])


