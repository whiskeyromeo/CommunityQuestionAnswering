"""
	2nd best performance, worse than implementation
	in doc2vec3.py
"""

from nltk.corpus import stopwords
from gensim import utils
from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument, Doc2Vec

from random import shuffle
from pprint import pprint
import csv
import re
import nltk
import logging
import numpy
import os
import sys
import pickle
from pathlib import Path 

sys.path.insert(0, os.path.abspath('..'))
from utils.sourceFiles import thisList, QTL_List, subTaskAList, origQfilePath, subtaskATestFilePath
from utils.QuestionFileCreator import QuestionCleaner, getQuestions, getComments, prepModelFolder, initializeLog
from utils.QuestionFileCreator import getQuestionsFromQTL, getCommentsFromQTL
from utils.QuestionFileCreator import filterPunctuation
from utils.cosineSimilarity import cosineSimilarity
from utils.elementParser import elementParser, originalQuestionParser

from utils.DataParser import DataParser as DP

initializeLog()

stops = set(stopwords.words('english'))

'''
	Preps the list of TaggedDocs to be fed into Doc2Vec
'''
def prepLabeledSentList(questions = []):
	mod_questions = []
	# for each of the questions create a TaggedDoc, append to the new list
	for q in questions:
		mod_questions.append(TaggedDocument([i for i in q['question'].lower().split() if i not in stops], (q['id'])))
	return mod_questions


'''
	Memory friendly implementation of Doc2Vec with decreasing learning rate to reduce decay
'''
def RareDoc2Vec(questions):
	mod_questions = prepLabeledSentList(questions)
	model = Doc2Vec(alpha=0.025, min_alpha=0.025)  # use fixed learning rate
	model.build_vocab(mod_questions)
	for epoch in range(10):
	    model.train(mod_questions)
	    model.alpha -= 0.002  # decrease the learning rate
	    model.min_alpha = model.alpha  # fix the learning rate, no decay
	#model.save('./tmp/RareModel')
	return model


'''
	Sets the doc2vec vectors for each of the questions
'''
def setVectors(hashList, model):
	for q in hashList:
		q['D2V_qVec1'] = model.infer_vector(q['question'])


def combineDocumentData(task3HashList, QTLHashList, comments=False):
	docs = DP.getQuestions(task3HashList)
	docs += DP.getQuestionsFromQTL(QTLHashList)
	if(comments):
		docs += DP.getComments(task3HashList)
		docs += DP.getCommentsFromQTL(QTLHashList)
	return docs


'''
	Modifies the hashmap to incorporate the doc2vec output for each question
'''
def BuildDoc2VecMap(questions):
	# clean the questions, removing punctuation and whitespace
	questions = QuestionCleaner(questions)
	# Create the Doc2Vec Model
	model = RareDoc2Vec(questions)
	# Set the vectors back in the hashmap
	#setVectors(hashmap, model)
	return model


if not os.path.isdir('tmp'):
	os.makedirs('tmp')


#Generate The models for comparison
if(Path("tmp/d2v1_model.p").is_file()):
	model = pickle.load(open("tmp/d2v1_model.p", "rb"))
else:
	#Build the model based on the Competition Question data
	questions = getQuestions(thisList)
	model = BuildDoc2VecMap(questions)
	pickle.dump(model, open("tmp/d2v1_model.p", "wb"))

if(Path("tmp/d2v1C_model.p").is_file()):
	model_c = pickle.load(open("tmp/d2v1C_model.p", "rb"))
else:
	# Build model based on Competition Question and Comment Data
	questions = getQuestions(thisList)
	questions += getComments(thisList)
	model_c = BuildDoc2VecMap(questions)
	pickle.dump(model_c, open("tmp/d2v1C_model.p", "wb"))


if(Path("tmp/d2v1_model_QTL.p").is_file()):
	modelQTL = pickle.load(open("tmp/d2v1_model_QTL.p", "rb"))
else:
	# Build the model based on the Competition and Crawler Question Data
	questions = combineDocumentData(thisList, QTL_List)
	modelQTL = BuildDoc2VecMap(questions)
	pickle.dump(modelQTL, open("tmp/d2v1_model_QTL.p", "wb"))


if(Path("tmp/d2v1_model_QTL_C.p").is_file()):
	modelQTL_C = pickle.load(open("tmp/d2v1_model_QTL_C.p", "rb"))
else:
	# Build the model based on the Competition and Crawler Question and Comment Data
	questionComments = combineDocumentData(subTaskAList, QTL_List, True)
	modelQTL_C = BuildDoc2VecMap(questionComments)
	pickle.dump(modelQTL_C, open("tmp/d2v1_model_QTL_C.p", "wb"))

"""
	Create a list of vectors with a 1/1 match for each question in questionList
"""
def getVectors(questionList):
	vecList = []
	for vecs in questionList:
		vecList.append(vecs["D2V_qVec1"])
	return vecList

"""
	Create a prediction file
	Arguments:
		filePath : Should be a filepath which conforms to the structure needed for the originalQuestionParser
		questionList : Should be a list of hashes containing the information about the provided questions
	Output:
		file: takes the filename from the filePath and saves a .pred file based on that name
		containing the information needed to run the MAP against it 
"""
def createPredictionFile(filePath, model, withStops=True, fileTag=''):
	testQuestions = originalQuestionParser(filePath)
	head, tail = os.path.split(filePath)
	tail = tail.split('.')[0]
	if(len(fileTag) > 0):
		fileTag = '-' + fileTag + '-'
	if(withStops):
		predFile = tail + '-d2v-with-stops' + fileTag + '.pred'
	else:
		predFile = tail + '-d2v' + fileTag + '.pred'
	modelPath = prepModelFolder()
	predFile = modelPath + predFile
	with open(predFile, "w") as tsvfile:
		writer = csv.writer(tsvfile, delimiter="\t")
		for t_question in testQuestions:
			t_question['origQuestion'] = filterPunctuation(t_question['origQuestion'])
			if(withStops):
				t_question['D2V_OVec1'] = model.infer_vector(t_question['origQuestion'])
			else: 
				t_question['origQNoStops'] = " ".join([i for i in t_question['origQuestion'].lower().split() if i not in stops])
				t_question['D2V_OVec1'] = model.infer_vector(t_question['origQNoStops'])

			vecList = []
			for rel_quest in t_question['rel_questions']:
				rel_quest['question'] = filterPunctuation(rel_quest['question'])
				if(withStops):
					rel_quest['D2V_qVec1'] = model.infer_vector(rel_quest['question'])
				else:
					rel_quest['relQNoStops'] = " ".join([i for i in rel_quest['question'].lower().split() if i not in stops])
					rel_quest['D2V_qVec1'] = model.infer_vector(rel_quest['relQNoStops'])
				vecList.append(rel_quest['D2V_qVec1'])		
			simMatrix = cosineSimilarity(t_question['D2V_OVec1'], vecList)
			for idx, row in enumerate(t_question['rel_questions']):
				row['simVal'] = simMatrix[idx]
				writer.writerow([t_question['quest_ID'], row['rel_quest_ID'], 0, row['simVal'], row['relevant']])
				

def createD2VPredictionFileSubTaskA(filePath, model, withStops=True, fileTag=''):
	testQuestions = elementParser(filePath)
	head, tail = os.path.split(filePath)
	tail = tail.split('.')[0]
	if(len(fileTag) > 0):
		fileTag = '-' + fileTag + '-'
	if(withStops):
		predFile = tail + '-d2v-with-stops' + fileTag+ '.pred'
	else:
		predFile = tail + '-d2v' + fileTag +'.pred'
	modelPath = prepModelFolder()
	predFile = modelPath + predFile
	with open(predFile, "w") as tsvfile:
		writer = csv.writer(tsvfile, delimiter="\t")
		for t_question in testQuestions:
			t_question['question'] = filterPunctuation(t_question['question'])
			if(withStops):
				t_question['D2V_qVec1'] = model.infer_vector(t_question['question'])
			else:
				t_question['relQNoStops'] = " ".join([i for i in t_question['question'].lower().split() if i not in stops])
				t_question['D2V_qVec1'] = model.infer_vector(t_question['relQNoStops'])
			vecList = []
			for t_comment in t_question['comments']:
				t_comment['comment'] = filterPunctuation(t_comment['comment'])
				if(withStops):
					t_comment['D2V_cVec1'] = model.infer_vector(t_comment['comment'])		
				else:
					t_comment['relCNoStops'] = " ".join([i for i in t_comment['comment'].lower().split() if i not in stops])
					t_comment['D2V_cVec1'] = model.infer_vector(t_comment['relCNoStops'])
				vecList.append(t_comment['D2V_cVec1'])
			simMatrix = cosineSimilarity(t_question['D2V_qVec1'], vecList)
			for idx, row in enumerate(t_question['comments']):
				row['simVal'] = simMatrix[idx]
				writer.writerow([t_question['threadId'], row['comment_id'], 0, row['simVal'], row['comment_rel']])



# # Develop prediction file for Subtask B on solely the Competition Question set
# createPredictionFile(origQfilePath, model, False)
# createPredictionFile(origQfilePath, model)


# # Develop prediction file for SubtaskB on solely the questions and crawler Data
# createPredictionFile(origQfilePath, modelQTL, False, 'crawlerModel')
# createPredictionFile(origQfilePath, modelQTL, True, 'crawlerModel')


# # Develop prediction file for subtask A based on all of the questions and comments
# createD2VPredictionFileSubTaskA(subtaskATestFilePath, modelQTL_C, True,'crawlComModel')
# createD2VPredictionFileSubTaskA(subtaskATestFilePath, modelQTL_C, False, 'crawlComModel')

# # Develop prediction files for subTask B based on all of the questions and comments
# createPredictionFile(origQfilePath, modelQTL_C, False, 'crawlComModel')
# createPredictionFile(origQfilePath, modelQTL_C, True, 'crawlComModel')


