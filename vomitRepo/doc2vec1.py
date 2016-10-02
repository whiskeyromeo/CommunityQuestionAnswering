from gensim import utils
from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument, LabeledSentence, Doc2Vec
from QuestionFileCreator import QuestionCleaner
import re
import logging

from nltk.corpus import stopwords
import numpy
from random import shuffle
from sklearn.linear_model import LogisticRegression
from whiskeyPrimer2 import thisList



def getQuestions(hashmap):
	questions = []
	for row in hashmap:
		qData = {
			"id": row["threadId"],
			"question": row["question"] 
		}
		questions.append(qData)
	return questions

questions = getQuestions(thisList)


# mod_questions = []
# for idx, question in enumerate(questions):
# 	mod_questions.append(LabeledSentence(re.sub('[^a-zA-Z]',' ',question).lower().split(), ("SENT_" + str(idx))))

# model = Doc2Vec(mod_questions, size=100, window=8, min_count=5, workers=4)
# model_name = 'doc2vec_size100_window8_min5_work4'
# model.save('./tmp/' + model_name)


def prepLabeledSentList(questions = []):
	mod_questions = []
	for idx, question in enumerate(questions):
		#print 'idx: ' + str(idx) + ' , question: ' + question
		mod_questions.append(TaggedDocument([i for i in question.lower().split() if i not in stops], ("SENT_" + str(idx))))
	return mod_questions

def prepModel(mod_questions, size=100, window=8, minCount=5, workers=4):
	model = Doc2Vec(mod_questions, size=size, window=window, min_count=minCount, workers=workers)
	model_name = 'doc2vec_size{}window{}min{}work{}'.format(size, window, minCount, workers)
	model.save('./tmp/'+ model_name)
	return model

def altDoc2Vec(questions):
	mod_questions = prepLabeledSentList(questions)
	model = Doc2Vec(min_count=1, window=10, size=100, sample=1e-4, negative=5, workers=8)
	model.build_vocab(mod_questions)
	shuffle(mod_questions)

	for epoch in range(10):
		model.train(mod_questions)

	model.save('./tmp/doc2vec_size100window10min5work4samp1e-4')

	


def RareDoc2Vec(questions):
	mod_questions = prepLabeledSentList(questions)
	model = Doc2Vec(alpha=0.025, min_alpha=0.025)  # use fixed learning rate
	model.build_vocab(mod_questions)
	for epoch in range(10):
	    model.train(mod_questions)
	    model.alpha -= 0.002  # decrease the learning rate
	    model.min_alpha = model.alpha  # fix the learning rate, no decay
