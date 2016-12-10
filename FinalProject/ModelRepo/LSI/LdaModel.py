'''
	Relies on some of the code from LsiModel.py to generate prediction files for a LDA model
	This was not included in the prediction files and was developed as an aside to the main project

	__author__ = Will Russell

'''


from gensim import corpora, models, similarities
from six import iteritems
from nltk.corpus import stopwords
import logging
import os
import re
import csv
import sys
from pathlib import Path


sys.path.insert(0, os.path.abspath('..'))
from utils.QuestionFileCreator import CreateFilePath, getQuestions, getComments, QuestionCleaner, initializeLog, prepModelFolder
from utils.elementParser import elementParser, originalQuestionParser
from utils.sourceFiles import thisList, origQfilePath
from LSIModel import generateDictionaries

initializeLog()

SemDictionary, SemCDictionary, QTLDictionary, QTLCDictionary = generateDictionaries()


'''

'''
def generateLDAModel(corpus, dictionary, numTopics=200):
	corpora.MmCorpus.serialize(new_dest + '.mm', corpus)
	serialized_corpus = corpora.MmCorpus(new_dest + '.mm')
	tfidf = models.TfidfModel(corpus)
	corpus_tfidf = tfidf[corpus]
	lda = models.ldamodel.LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=100, update_every=0, passes=20)
	index = similarities.MatrixSimilarity(lda[serialized_corpus])
	return lda, index



'''

'''
def createLDAPredictionFile(filePath, dictionary, numFeatures=200, withStops=True, fileTag=''):
	testQuestions = originalQuestionParser(filePath)
	head, tail = os.path.split(filePath)
	tail = tail.split('.')[0]
	if(len(fileTag) > 0):
		fileTag = '-' + fileTag + '-'
	if(withStops):
		predFile = tail +'-lda' + str(numFeatures) +'-with-stops.pred'
	else:
		predFile = tail + '-lda' + str(numFeatures) + '.pred'
	modelPath = prepModelFolder()
	predFile = modelPath + predFile
	with open(predFile, 'w') as tsvfile:
		writer = csv.writer(tsvfile, delimiter='\t')
		for t_question in testQuestions:
			t_question['origQuestion'] = filterPunctuation(t_question['origQuestion'])
			corpus = []
			for rel_quest in t_question['rel_questions']:
				rel_quest['question'] = filterPunctuation(rel_quest['question'])
				corpus.append(dictionary.doc2vow(rel_quest['question'].lower().word_tokenize()))
			#corpus = [dictionary.doc2bow(q['question'].lower().word_tokenize()) for q in t_question['rel_questions']]
			lda, index = generateLDAModel(corpus, dictionary, numFeatures)
			if(withStops):
				doc = t_question['origQuestion']
			else: 
				t_question['origQNoStops'] = " ".join([i for i in t_question['origQuestion'].lower().word_tokenize() if i not in stops])
				doc = t_question['origQNoStops']
			vec_bow = dictionary.doc2bow(doc.lower().word_tokenize())
			vec_lda = lda[vec_bow]
			sims = index[vec_lda]
			for idx, quest in enumerate(t_question['rel_questions']):
				quest['simVal'] = sims[idx]
				writer.writerow([t_question['quest_ID'], quest['rel_quest_ID'], idx, quest['simVal'], quest['relevant']])


'''

'''
def createLSIPredictionFileSubTaskA(filePath, dictionary, numFeatures=200, withStops=True, fileTag=''):
	testQuestions = elementParser(filePath)
	head, tail = os.path.split(filePath)
	tail = tail.split('.')[0]
	if(len(fileTag) > 0):
		fileTag = '-' + fileTag + '-'
	if(withStops):
		predFile = tail + '-lda' + str(numFeatures) + '-with-stops' + fileTag + '.pred'
	else:
		predFile = tail + '-lda' + str(numFeatures) + fileTag +'.pred'
	modelPath = prepModelFolder()
	with open(predFile,'w') as tsvfile:
		writer = csv.writer(tsvfile, delimiter='\t')
		for t_question in testQuestions:
			t_question['question'] = filterPunctuation(t_question['question'])
			corpus = []
			for rel_comment in t_question['comments']:
				rel_comment['comment'] = filterPunctuation(rel_comment['comment'])
				corpus.append(dictionary.doc2bow(doc.lower().word_tokenize()))
			lda, index = generateLDAModel(corpus, dictionary, numFeatures)
			if(withStops):
				doc = t_question['question']
			else:
				t_question['question'] = ' '.join([i for i in t_question['question'] if i not in stops])
				doc = t_question['question']
			vec_bow = dictionary.doc2bow(doc.lower().word_tokenize())
			vec_lda = lda[vec_bow]
			sims = index[vec_lda]
			for idx, quest in enumerate(t_question['comments']):
				quest['simVal'] = sims[idx]
				writer.writerow([t_question['threadId'], row['comment_id'], 0, row['simVal'], row['comment_rel']])


createLDAPredictionFile(origQfilePath, SemDictionary, 100, False)


