from gensim import utils
from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument, LabeledSentence, Doc2Vec
from QuestionFileCreator import QuestionCleaner, getQuestions
import re
import logging

from nltk.corpus import stopwords
import numpy
from random import shuffle
from sklearn.linear_model import LogisticRegression
from whiskeyPrimer2 import thisList
from cosineSimilarity import cosineSimilarity
from elementParser import originalQuestionParser
import csv
from pprint import pprint

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

questions = getQuestions(thisList)
mod_questions = prepLabeledSentList(questions)

model = BuildDoc2VecMap(thisList)

vecList = []
for vecs in thisList:
	vecList.append(vecs["D2V_qVec1"])


simMatrix = cosineSimilarity(vecList[0], vecList)

for idx,row in enumerate(thisList):
	row["simVal"] = simMatrix[idx]

##### EndProof ##################

# TODO:
# Write a function to run modified elementParser over
# the TestFile to pull the Ids of the relevant question.
# Need to step by 10 to pull each question_id 
# Returns : a list of the questions and their ids

origQfilePath = '../Data/english_scorer_and_random_baselines_v2.2/SemEval2016-Task3-CQA-QL-dev.xml'

testQuestions = originalQuestionParser(origQfilePath)


# TODO : Convert to function following code
# thisperforms construction of tsv file from output of previous function
# Output Format:
# 	<ORIG_Q> <TEST_Q> <RANK> <COSINE> <RELEVANT Y/N>
with open("./record.pred","w") as tsvfile: 
	writer = csv.writer(tsvfile, delimiter='\t')
	for t_question in testQuestions[:10]:
		t_question['origQNoStops'] = " ".join([i for i in t_question['origQuestion'].lower().split() if i not in stops])
		t_question['D2V_OVec1'] = model.infer_vector(t_question['origQNoStops'])
		simMatrix = cosineSimilarity(t_question['D2V_OVec1'], vecList)
		for idx, row in enumerate(thisList):
			row['simVal'] = simMatrix[idx]
		newList = sorted(thisList, key=lambda x:x['simVal'], reverse=True)
		count = 1
		for question in newList[:10]:
			if(question['simVal'] < 0.9):
				rel = False
			else:
				rel = True
			writer.writerow([t_question['quest_ID'], question['threadId'], count, question['simVal'], rel])
			count += 1


### Alternative DOC2VEC IMPLEMENTATIONS ##########


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
