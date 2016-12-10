'''
	This file creates prediction files based on Word2Vec word averaging to develop vectors
	for documents. Performance on Subtask B was poor when compared with LSI, however performance on 
	Subtask A was better than the other methods analyzed


	__author__ = Will Russell
'''


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

sys.path.insert(0, os.path.abspath('..'))
from crawler.jsonDumper import createObjectListFromJson
from utils.sourceFiles import thisList, origQfilePath, subtaskATestFilePath
from utils.cosineSimilarity import cosineSimilarity
from utils.QuestionFileCreator import getQuestionsFromQTL, getCommentsFromQTL, getQuestions, prepModelFolder, filterPunctuation
from utils.elementParser import elementParser, originalQuestionParser
from vectorTools import buildQuestionMap, generateTokens, generateAvgVectors, generateQuestionVector

stops = set(stopwords.words('english'))

#Generate the dimensions for the word2vec model
DIM = 600
TOKEN_LIMIT = 30000
WORKERS = 8
WINDOW = 10
DYNAMIC_WINDOW = False
NEGATIVE = 10

'''
	Need to generate a set of functions which can create a model based on the vocabulary derived from both the crawler json files and the xml files
'''

QTLfilePaths = [
	'../crawler/data/questFile.json',
	'../crawler/data/questFile2.json',
	'../crawler/data/questFile3.json',
	'../crawler/data/questFile4.json'
]


def generateQuestionDataForW2VModel():
	questionList = []
	questions = generateTask3QuestionData(thisList)
	qtlData = generateQTLData(QTLfilePaths)
	questions += generateQTLQuestionData(qtlData)
	for q in questions:
		questionList.append(q['word_tokens'])
	return questionList

def generateQTLData(filePaths):
	qtlData = []
	for filePath in filePaths:
		qtlData += createObjectListFromJson(filePath)
	return qtlData

def generateQTLQuestionData(qtlData):
	qtlQuestions = getQuestionsFromQTL(qtlData)
	generateTokens(qtlQuestions)
	return qtlQuestions

def generateQTLCommentData(qtlData):
	qtlComments = getCommentsFromQTL(qtlData)
	generateTokens(qtlComments)
	return qtlComments

def generateCommentDataForModel():
	commentList = []
	qtlData = generateQTLData(QTLfilePaths)
	comments = generateTask3CommentData(thisList)
	comments += generateQTLCommentData(qtlData)
	for c in comments:
		commentList.append(q['word_tokens'])
	return commentList

def generateTask3CommentData(hashList):
	comments = getComments(hashList)
	generateTokens(comments)
	return comments

def generateTask3QuestionData(hashList):
	questions = getQuestions(hashList)
	generateTokens(questions)
	return questions


# This seems to be the ideal sampling method based on the gensim team comparison
if(Path("tmp/w2v1_model.p").is_file()):
	print("Model found! Loading...")
	model = pickle.load(open("tmp/w2v1_model.p", "rb"))
else:
	print("No model found! Entering the jungle....")
	questionList = generateQuestionDataForW2VModel()
	id2word = gensim.corpora.Dictionary(questionList)
	word2id = dict((v,k) for k,v in id2word.iteritems())
	corpus = lambda: ([word.lower() for word in question if word in word2id] for question in questionList)
	model = Word2Vec(size=DIM, window=WINDOW, workers=WORKERS,hs=0,negative=NEGATIVE)
	model.build_vocab(corpus())
	model.train(corpus())
	#Done training the model
	model.init_sims(replace=True)
	pickle.dump(model, open("tmp/w2v1_model.p", "wb"))


def createW2VPredictionFile(filePath, model, withStops=True):
	testQuestions = originalQuestionParser(filePath)
	head, tail = os.path.split(filePath)
	tail = tail.split('.')[0]
	if(withStops):
		predFile = tail + '-w2v-with-stops.pred'
	else:
		predFile = tail + '-w2v.pred'
	modelPath = prepModelFolder()
	predFile = modelPath + predFile
	with open(predFile, "w") as tsvfile:
		writer = csv.writer(tsvfile, delimiter="\t")
		for t_question in testQuestions:
			t_question['origQuestion'] = filterPunctuation(t_question['origQuestion'])
			if(withStops):
				t_question['origQuestion'] = filterPunctuation(t_question['origQuestion'])
				t_question['W2V_OVec1'] = generateQuestionVector(model,t_question['origQuestion'], DIM)
			else: 
				t_question['origQNoStops'] = " ".join([i for i in t_question['origQuestion'].lower().split() if i not in stops])
				t_question['W2V_OVec1'] = generateQuestionVector(model,t_question['origQNoStops'], DIM)

			vecList = []
			for rel_quest in t_question['rel_questions']:
				rel_quest['question'] = filterPunctuation(rel_quest['question'])
				if(withStops):
					rel_quest['W2V_qVec1'] = generateQuestionVector(model,rel_quest['question'], DIM)
				else:
					rel_quest['relQNoStops'] = " ".join([i for i in rel_quest['question'].lower().split() if i not in stops])
					rel_quest['W2V_qVec1'] = generateQuestionVector(model,rel_quest['relQNoStops'], DIM)
				vecList.append(rel_quest['W2V_qVec1'])		
			simMatrix = cosineSimilarity(t_question['W2V_OVec1'], vecList)
			for idx, row in enumerate(t_question['rel_questions']):
				row['simVal'] = simMatrix[idx]
				writer.writerow([t_question['quest_ID'], row['rel_quest_ID'], 0, row['simVal'], row['relevant']])



#Need to use with dev-subtaskA.xml file --> subtaskATestFilePath
def createW2VPredictionFileSubTaskA(filePath, model, withStops=True):
	testQuestions = elementParser(filePath)
	head, tail = os.path.split(filePath)
	tail = tail.split('.')[0]
	if(withStops):
		predFile = tail + '-w2v-with-stops.pred'
	else:
		predFile = tail + '-w2v.pred'
	modelPath = prepModelFolder()
	predFile = modelPath + predFile
	with open(predFile, "w") as tsvfile:
		writer = csv.writer(tsvfile, delimiter="\t")
		for t_question in testQuestions:
			t_question['question'] = filterPunctuation(t_question['question'])
			if(withStops):
				t_question['W2V_qVec1'] = generateQuestionVector(model,t_question['question'], DIM)
			else:
				t_question['relQNoStops'] = " ".join([i for i in t_question['question'].lower().split() if i not in stops])
				t_question['W2V_qVec1'] = generateQuestionVector(model,t_question['relQNoStops'], DIM)
			vecList = []
			for t_comment in t_question['comments']:
				t_comment['comment'] = filterPunctuation(t_comment['comment'])
				if(withStops):
					t_comment['W2V_cVec1'] = generateQuestionVector(model, t_comment['comment'], DIM)
				else:
					t_comment['relCNoStops'] = " ".join([i for i in t_comment['comment'].lower().split() if i not in stops])
					t_comment['W2V_cVec1'] = generateQuestionVector(model, t_comment['relCNoStops'], DIM)
				vecList.append(t_comment['W2V_cVec1'])
			simMatrix = cosineSimilarity(t_question['W2V_qVec1'], vecList)
			for idx, row in enumerate(t_question['comments']):
				row['simVal'] = simMatrix[idx]
				writer.writerow([t_question['threadId'], row['comment_id'], 0, row['simVal'], row['comment_rel']])


createW2VPredictionFile(origQfilePath, model, False)
createW2VPredictionFile(origQfilePath, model)

createW2VPredictionFileSubTaskA(subtaskATestFilePath, model, False)
createW2VPredictionFileSubTaskA(subtaskATestFilePath, model)

