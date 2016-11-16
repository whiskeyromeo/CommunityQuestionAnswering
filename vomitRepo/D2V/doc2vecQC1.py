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
import logging
import numpy
import os
import pickle
from pathlib import Path

sys.path.insert(0, os.path.abspath('..'))
from utils.QuestionFileCreator import QuestionCleaner, getQuestions, prepModelFolder, initializeLog
from utils.cosineSimilarity import cosineSimilarity
from utils.elementParser import elementParser, originalQuestionParser
from utils.sourceFiles import thisList, origQfilePath
from D2V.doc2vec1 import prepLabeledSentList, RareDoc2Vec, setVectors, BuildDoc2VecMap, getVectors

stops = set(stopwords.words('english'))


#NOTE: The following may need to be uncommented for this file to work
if(Path("tmp/d2vqc1_model.p").is_file()):
	model = pickle.load(open("tmp/d2vqc1_model.p", "rb"))
else:
	model = BuildDoc2VecMap(thisList)
	pickle.dump(model, open("tmp/d2vqc1_model.p", "wb"))

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
	testQuestions = originalQuestionParser(filePath)
	head, tail = os.path.split(filePath)
	tail = tail.split('.')[0]
	if(withStops):
		predFile = tail + '-d2v-qc-with-stops.pred'
	else:
		predFile = tail + '-d2v-qc.pred'
	modelPath = prepModelFolder()
	predFile = modelPath + predFile
	with open(predFile, "w") as tsvfile:
		writer = csv.writer(tsvfile, delimiter="\t")
		for t_question in testQuestions:
			if(withStops):
				t_question['D2V_OVec1'] = model.infer_vector(t_question['origQuestion'])
			else: 
				t_question['origQNoStops'] = " ".join([i for i in t_question['origQuestion'].lower().split() if i not in stops])
				t_question['D2V_OVec1'] = model.infer_vector(t_question['origQNoStops'])

			vecList = []
			for rel_quest in t_question['rel_questions']:
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
				

#createPredictionFile(origQfilePath, model, False)
#createPredictionFile(origQfilePath, model)


