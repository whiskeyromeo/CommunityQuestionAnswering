from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument, LabeledSentence, Doc2Vec
from QuestionFileCreator import QuestionCreator
from whiskeyPrimer2 import filePaths
import re
import logging


filename = 'myfile.txt'
questions = QuestionCreator(filePaths)
# mod_questions = []
# for idx, question in enumerate(questions):
# 	mod_questions.append(LabeledSentence(re.sub('[^a-zA-Z]',' ',question).lower().split(), ("SENT_" + str(idx))))

# model = Doc2Vec(mod_questions, size=100, window=8, min_count=5, workers=4)
# model_name = 'doc2vec_size100_window8_min5_work4'
# model.save('./tmp/' + model_name)

def prepLabeledSentList(questions = []):
	mod_questions = []
	for idx, question in enumerate(questions):
		print 'idx: ' + str(idx) + ' , question: ' + question
		mod_questions.append(TaggedDocument(re.sub('[^\w\s]',' ',question).lower().split(), ("SENT_" + str(idx))))
	return mod_questions

def prepModel(mod_questions, size=100, window=8, minCount=5, workers=4):
	model = Doc2Vec(mod_questions, size=size, window=window, min_count=minCount, workers=workers)
	return model





# From Rare Technologies Blog
# model = Doc2Vec(alpha=0.025, min_alpha=0.025)  # use fixed learning rate
# model.build_vocab(mod_questions)
# for epoch in range(10):
#     model.train(mod_questions)
#     model.alpha -= 0.002  # decrease the learning rate
#     model.min_alpha = model.alpha  # fix the learning rate, no decay
