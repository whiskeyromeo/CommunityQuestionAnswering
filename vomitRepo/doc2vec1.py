from nltk.corpus import stopwords

from gensim import utils
from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument, LabeledSentence, Doc2Vec

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


stops = set(stopwords.words('english'))

filePaths = [
	'../Data/train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-train-reformatted-excluding-2016-questions-cleansed.xml',
	'../Data/train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-dev-reformatted-excluding-2016-questions-cleansed.xml',
	'../Data/train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-test-reformatted-excluding-2016-questions-cleansed.xml',
	#All of the following contain OrigQuestions...not relevant
	#'../Data/dev/SemEval2016-Task3-CQA-QL-dev-subtaskA.xml',
	#'../Data/train/SemEval2016-Task3-CQA-QL-train-part2-subtaskA.xml',
	#'../Data/train/SemEval2016-Task3-CQA-QL-train-part1-subtaskA.xml'
]

thisList = []

for filePath in filePaths:
	thisList += elementParser(filePath)


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
	model.save('./tmp/RareModel')
	return model


'''
	Sets the doc2vec vectors for each of the questions
'''
def setVectors(hashmap, model):
	for q in hashmap:
		q['D2V_qVec1'] = model.infer_vector(q['question'])


'''
	Modifies the hashmap to incorporate the doc2vec output for each question
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


#### Proof of Concept ###########

model = BuildDoc2VecMap(thisList)

# vecList = []
# for vecs in thisList:
# 	vecList.append(vecs["D2V_qVec1"])


# simMatrix = cosineSimilarity(vecList[0], vecList)

# for idx,row in enumerate(thisList):
# 	row["simVal"] = simMatrix[idx]

##### EndProof ##################

# TODO:
# Write a function to run modified elementParser over
# the TestFile to pull the Ids of the relevant question.
# Need to step by 10 to pull each question_id 
# Returns : a list of the questions and their ids

origQfilePath = '../Data/english_scorer_and_random_baselines_v2.2/SemEval2016-Task3-CQA-QL-dev.xml'
questions = originalQuestionParser(origQfilePath)


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


def createPredictionFile(filePath, model, withStops=True):
	testQuestions = originalQuestionParser(filePath)
	head, tail = os.path.split(filePath)
	tail = tail.split('.')[0]
	if(withStops):
		predFile = tail + '-d2v-with-stops.pred'
	else:
		predFile = tail + '-d2v.pred'
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
				

createPredictionFile(origQfilePath, model, False)
createPredictionFile(origQfilePath, model)




# TODO : Convert to function following code
# thisperforms construction of tsv file from output of previous function
# Output Format:
# 	<ORIG_Q> <TEST_Q> <RANK> <COSINE> <RELEVANT Y/N>

# with open("./record.pred","w") as tsvfile: 
# 	writer = csv.writer(tsvfile, delimiter='\t')
# 	for t_question in testQuestions[:10]:
# 		t_question['origQNoStops'] = " ".join([i for i in t_question['origQuestion'].lower().split() if i not in stops])
# 		t_question['D2V_OVec1'] = model.infer_vector(t_question['origQNoStops'])
# 		simMatrix = cosineSimilarity(t_question['D2V_OVec1'], vecList)
# 		for idx, row in enumerate(thisList):
# 			row['simVal'] = simMatrix[idx]
# 		newList = sorted(thisList, key=lambda x:x['simVal'], reverse=True)
# 		count = 1
# 		for question in newList[:10]:
# 			if(question['simVal'] < 0.9):
# 				rel = False
# 			else:
# 				rel = True
# 			writer.writerow([t_question['quest_ID'], question['threadId'], count, question['simVal'], rel])
# 			count += 1


### Alternative DOC2VEC IMPLEMENTATIONS ##########

# questions = getQuestions(thisList)
# mod_questions = prepLabeledSentList(questions)


# mod_questions = []
# for idx, question in enumerate(questions):
# 	mod_questions.append(LabeledSentence(re.sub('[^a-zA-Z]',' ',question).lower().split(), ("SENT_" + str(idx))))

# model = Doc2Vec(mod_questions, size=100, window=8, min_count=5, workers=4)
# model_name = 'doc2vec_size100_window8_min5_work4'
# model.save('./tmp/' + model_name)


# def prepLabeledSentList(questions = []):
# 	mod_questions = []
# 	for idx, question in enumerate(questions):
# 		#print 'idx: ' + str(idx) + ' , question: ' + question
# 		mod_questions.append(TaggedDocument([i for i in question.lower().split() if i not in stops], ("SENT_" + str(idx))))
# 	return mod_questions


# def prepModel(mod_questions, size=100, window=8, minCount=5, workers=4):
# 	model = Doc2Vec(mod_questions, size=size, window=window, min_count=minCount, workers=workers)
# 	model_name = 'doc2vec_size{}window{}min{}work{}'.format(size, window, minCount, workers)
# 	model.save('./tmp/'+ model_name)
# 	return model


# def altDoc2Vec(questions):
# 	mod_questions = prepLabeledSentList(questions)
# 	model = Doc2Vec(min_count=1, window=10, size=100, sample=1e-4, negative=5, workers=8)
# 	model.build_vocab(mod_questions)
# 	shuffle(mod_questions)

# 	for epoch in range(10):
# 		model.train(mod_questions)

# 	model.save('./tmp/doc2vec_size100window10min5work4samp1e-4')
# 	return model
