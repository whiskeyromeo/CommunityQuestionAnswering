"""
	This file constructs a Doc2Vec model and outputs
	the prediction file based on cosineSimilarity measures
	derived from the vectors of questions
	
	This system performed better than the one implemented
	in doc2vec1.py

	__author__ = Will Russell
	
"""

from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from nltk.corpus import stopwords
import sys
import os
import pickle
from pathlib import Path

sys.path.insert(0, os.path.abspath('..'))
from utils.QuestionFileCreator import QuestionCleaner, initializeLog
from utils.QuestionFileCreator import getQuestionsFromQTL, QTLQuestionCreator
from utils.sourceFiles import thisList, QTL_List, subTaskAList, origQfilePath, subtaskATestFilePath
#from D2V.doc2vec1 import createPredictionFile
from utils.DataParser import DataParser as DP
from Doc2Vec1 import Doc2Vec1 as d2v

initializeLog()


stops = set(stopwords.words('english'))

"""
	Takes in a list of Questions and outputs a list of TaggedDocument objects
	Params:
		questions: a list of questions
		withStops: A boolean value representing whether to remove stops or not
	Returns:
		mod_questions: A list of TaggedDocument objects which consists of a list of words
			for each document and associated tags for each word

"""
def prepLabeledSentList(questions = [], withStops = False):
	mod_questions = []
	for q in questions:
		if not withStops:
			mod_questions.append(TaggedDocument([i for i in q['question'] if i not in stops], q['id']))
		else:
			mod_questions.append(TaggedDocument(q['question'], q['id']))
	return mod_questions


"""
	prepModel takes in a list of TaggedDocuments and parameters to be passed into 
	the creation of the Doc2Vec object and outputs a prepared Doc2Vec model
	Params:
		mod_questions : a list of TaggedDocuments
		size : The number of features to be used in the Doc2Vec model
		window : The window size
		minCount : The minimum count of each word to be taken into account in the model creation
		workers : Number of worker threads to use in creation of the model
"""
def prepModel(mod_questions, size=300, window=7, minCount=5, workers=4):
	model = Doc2Vec(mod_questions, size=size, window=window, min_count=minCount, workers=workers)
	return model


def buildDoc2Vec3Model(questions=[], size=300, window=7, minCount=5, workers=4, withStops=False):
	questions = QuestionCleaner(questions)
	mod_questions = prepLabeledSentList(questions)
	model = Doc2Vec(mod_questions, size=size, window=window, min_count=minCount, workers=workers)
	return model


print("Running 3rd implementation of Doc2Vec")

#Generate The models for comparison
if(Path("tmp/d2v3_model.p").is_file()):
	print('base SemEval question model found, loading...')
	model = pickle.load(open("tmp/d2v3_model.p", "rb"))
else:
	#Build the model based on the Competition Question data
	print('base SemEval question model not found, generating...')
	questions = DP.getQuestions(thisList)
	model = buildDoc2Vec3Model(questions)
	pickle.dump(model, open("tmp/d2v3_model.p", "wb"))

if(Path("tmp/d2v3C_model.p").is_file()):
	print('base SemEval question/comment model found, loading...')
	model_c = pickle.load(open("tmp/d2v3C_model.p", "rb"))
else:
	# Build model based on Competition Question and Comment Data
	print('base SemEval question/comment model not found, generating...')
	questions = DP.getQuestions(thisList)
	questions += DP.getComments(thisList)
	model_c = buildDoc2Vec3Model(questions)
	pickle.dump(model_c, open("tmp/d2v3C_model.p", "wb"))


if(Path("tmp/d2v3_model_QTL.p").is_file()):
	print('base QTL/SemEval question model found, loading...')
	modelQTL = pickle.load(open("tmp/d2v3_model_QTL.p", "rb"))
else:
	# Build the model based on the Competition and Crawler Question Data
	print('base QTL/SemEval question model not found, generating...')
	questions = DP.combineDocumentData(thisList, QTL_List)
	modelQTL = buildDoc2Vec3Model(questions)
	pickle.dump(modelQTL, open("tmp/d2v3_model_QTL.p", "wb"))


if(Path("tmp/d2v3_model_QTL_C.p").is_file()):
	print('base QTL/SemEval question/comment model found, loading...')
	modelQTL_C = pickle.load(open("tmp/d2v3_model_QTL_C.p", "rb"))
else:
	# Build the model based on the Competition and Crawler Question and Comment Data
	print('base QTL/SemEval question/comment model not found, generating...')
	questionComments = DP.combineDocumentData(subTaskAList, QTL_List, True)
	modelQTL_C = buildDoc2Vec3Model(questionComments)
	pickle.dump(modelQTL_C, open("tmp/d2v3_model_QTL_C.p", "wb"))




print('Creating DOC2VEC-3 Prediction Models')

# Prep the predictive models
d2v.createPredictionFile(origQfilePath, model, True, 'v3-SEM')
d2v.createPredictionFile(origQfilePath, model, False, 'v3-SEM')

d2v.createPredictionFile(origQfilePath, model_c, True, 'v3-SEMC')
d2v.createPredictionFile(origQfilePath, model_c, False, 'v3-SEMC')

d2v.createPredictionFile(origQfilePath, modelQTL, True, 'v3-SEMQTL')
d2v.createPredictionFile(origQfilePath, modelQTL, False, 'v3-SEMQTL')


