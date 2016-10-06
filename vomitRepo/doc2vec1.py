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


questions = getQuestions(thisList)
mod_questions = prepLabeledSentList(questions)

model = BuildDoc2VecMap(thisList)

vecList = []
for vecs in thisList:
	vecList.add(vecs["D2V_qVec1"])




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
