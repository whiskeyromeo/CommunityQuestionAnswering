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
from utils.sourceFiles import thisList, origQfilePath
from utils.cosineSimilarity import cosineSimilarity
from utils.QuestionFileCreator import getQuestionsFromQTL, getQuestions, prepModelFolder
from utils.elementParser import originalQuestionParser
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

qtlQuestions = createObjectListFromJson('../crawler/data/questFile.json')
qtlQuestions += createObjectListFromJson('../crawler/data/questFile2.json')
qtlQuestions += createObjectListFromJson('../crawler/data/questFile3.json')
qtlQuestions += createObjectListFromJson('../crawler/data/questFile4.json')
qtlQuestions = getQuestionsFromQTL(qtlQuestions)

generateTokens(qtlQuestions)
questions = getQuestions(thisList)
generateTokens(questions)

questionList = []
for q in questions:
	questionList.append(q['question_tokens'])
for q in qtlQuestions:
	questionList.append(q['question_tokens'])
	
id2word = gensim.corpora.Dictionary(questionList)
word2id = dict((v,k) for k,v in id2word.iteritems())
corpus = lambda: ([word.lower() for word in question if word in word2id] for question in questionList)

# This seems to be the ideal sampling method based on the gensim team comparison
model = Word2Vec(size=DIM, window=WINDOW, workers=WORKERS,hs=0,negative=NEGATIVE)
model.build_vocab(corpus())
model.train(corpus())


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
			if(withStops):
				t_question['W2V_OVec1'] = generateQuestionVector(model,t_question['origQuestion'], DIM)
			else: 
				t_question['origQNoStops'] = " ".join([i for i in t_question['origQuestion'].lower().split() if i not in stops])
				t_question['W2V_OVec1'] = generateQuestionVector(model,t_question['origQNoStops'], DIM)

			vecList = []
			for rel_quest in t_question['rel_questions']:
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

createW2VPredictionFile(origQfilePath, model, False)
createW2VPredictionFile(origQfilePath, model)

