'''
	Generates prediction files for subtaskB using LSI 
	__author__ = Will Russell

'''
from gensim import corpora, models, similarities
from six import iteritems
from nltk.corpus import stopwords
from nltk import word_tokenize
import logging
import os
import re
import csv
import sys

from pathlib import Path

sys.path.insert(0, os.path.abspath('..'))
from utils.QuestionFileCreator import CreateFilePath, QuestionCleaner, filterPunctuation, prepModelFolder, initializeLog
from utils.elementParser import elementParser, originalQuestionParser
from utils.sourceFiles import thisList, QTL_List, subTaskAList, origQfilePath, subtaskATestFilePath
from utils.DataParser import DataParser as DP

initializeLog()

stops = set(stopwords.words('english'))

if not os.path.isdir('tmp'):
	os.makedirs('tmp')


def createDictionary(sources, fileName="LSIModel", fileTag=''):
	dictionary = corpora.Dictionary(word_tokenize(line['question'].lower()) for line in sources)
	stop_ids = [dictionary.token2id[stopword] for stopword in stops if stopword in dictionary.token2id]
	once_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq == 1]
	dictionary.filter_tokens(stop_ids + once_ids)
	dictionary.compactify()
	if(len(fileTag) > 0):
		fileTag = '-' + fileTag
	filename = fileName + fileTag + '.dict'
	print(filename)
	dictionary.save('tmp/' + filename)
	return dictionary


def generateDictionaries():
	# Create dictionary based on SemEval Questions
	if(Path("tmp/Sem.dict").is_file()):
		print('SemEval Question Dictionary Found')
		SemDictionary = models.LsiModel.load('tmp/Sem.dict')
	else:
		print('Creating SemEval Dictionary...')
		sources = QuestionCleaner(DP.getQuestions(thisList))
		SemDictionary = createDictionary(sources, 'Sem')

	# Create Dictionary based on SemEval Question + Comments
	if(Path("tmp/SemC.dict").is_file()):
		print('SemEval Question/Comment Dictionary Found')
		SemCDictionary = models.LsiModel.load('tmp/SemC.dict')
	else:
		print('Creating SemEval Question/Comment Dictionary...')
		sources = QuestionCleaner(DP.getQuestions(thisList))
		sources += QuestionCleaner(DP.getComments(thisList))
		SemCDictionary = createDictionary(sources, 'SemC')

	# Create Dictionary based on SemEval Questions + Crawler Questions
	if(Path("tmp/QTL.dict").is_file()):
		print('QatarLiving + SemEval Dictionary Found')
		QTLDictionary = models.LsiModel.load('tmp/QTL.dict')
	else:
		print('Creating QatarLiving + SemEval Question Dictionary...')
		sources = QuestionCleaner(DP.combineDocumentData(thisList, QTL_List))
		QTLDictionary = createDictionary(sources, 'QTL')

	# Create Dictionary based on SemEval Questions+Comments and Crawler Question+Comments
	if(Path("tmp/QTLC.dict").is_file()):
		print('QatarLiving + SemEval Question/Comment Dictionary Found')
		QTLCDictionary = models.LsiModel.load('tmp/QTLC.dict')
	else:
		print('Creating QatarLiving + SemEval Question/Comment Dictionary...')
		sources = QuestionCleaner(DP.combineDocumentData(thisList, QTL_List, True))
		QTLCDictionary = createDictionary(sources, 'QTLC')
	return SemDictionary, SemCDictionary, QTLDictionary, QTLCDictionary


SemDictionary, SemCDictionary, QTLDictionary, QTLCDictionary = generateDictionaries()



def generateLSIModel(corpus, dictionary, numTopics):
	print('####################')
	print(corpus)
	corpora.MmCorpus.serialize('LSIModel.mm', corpus)
	serialized_corpus = corpora.MmCorpus('LSIModel.mm')
	tfidf = models.TfidfModel(corpus)
	corpus_tfidf = tfidf[corpus]
	lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=numTopics)
	print('####################')
	print(lsi[serialized_corpus])
	index = similarities.MatrixSimilarity(lsi[corpus_tfidf])
	return lsi, index



def createLSIPredictionFile(filePath, dictionary, numFeatures=200, withStops=True, fileTag=''):
	testQuestions = originalQuestionParser(filePath)
	head, tail = os.path.split(filePath)
	tail = tail.split('.')[0]
	if(len(fileTag) > 0):
		fileTag = '-' + fileTag + '-'
	if(withStops):
		predFile = tail + '-lsi' + str(numFeatures) + '-with-stops' + fileTag + '.pred'
	else:
		predFile = tail + '-lsi' + str(numFeatures) + fileTag +'.pred'
	modelPath = prepModelFolder()
	predFile = modelPath + predFile
	with open(predFile, 'w') as tsvfile:
		writer = csv.writer(tsvfile, delimiter='\t')
		for t_question in testQuestions:
			t_question['origQuestion'] = filterPunctuation(t_question['origQuestion'])
			corpus = []
			count = 0
			for rel_quest in t_question['rel_questions']:
				rel_quest['question'] = filterPunctuation(rel_quest['question'])
				corpus.append(dictionary.doc2bow(word_tokenize(rel_quest['question'].lower())))
				# if(count < 5):
				# 	print('###############')
				# 	print(rel_quest['question'])
				# 	print(dictionary.doc2bow(word_tokenize(rel_quest['question'].lower())))
				# 	count += 1
			#corpus = [dictionary.doc2bow(q['question'].lower().word_tokenize()) for q in t_question['rel_questions']]
			#print(corpus)
			lsi, index = generateLSIModel(corpus, dictionary, numFeatures)
			if(withStops):
				doc = t_question['origQuestion']
			else: 
				t_question['origQNoStops'] = " ".join([i for i in word_tokenize(t_question['origQuestion'].lower()) if i not in stops])
				doc = t_question['origQNoStops']
			vec_bow = dictionary.doc2bow(word_tokenize(doc.lower()))
			vec_lsi = lsi[vec_bow]
			sims = index[vec_lsi]
			for idx, quest in enumerate(t_question['rel_questions']):
				quest['simVal'] = sims[idx]
				writer.writerow([t_question['quest_ID'], quest['rel_quest_ID'], idx, quest['simVal'], quest['relevant']])


'''
	Not sure why but the implementation of SubtaskA with LSI fails horribly
	I have included the .pred files in this directory to demonstrate some of what we ran into
'''
def createLSIPredictionFileSubTaskA(filePath, dictionary, numFeatures=200, withStops=True, fileTag=''):
	testQuestions = elementParser(filePath)
	head, tail = os.path.split(filePath)
	tail = tail.split('.')[0]
	if(len(fileTag) > 0):
		fileTag = '-' + fileTag + '-'
	if(withStops):
		predFile = tail + '-lsi' + str(numFeatures) + '-with-stops' + fileTag + '.pred'
	else:
		predFile = tail + '-lsi' + str(numFeatures) + fileTag +'.pred'
	modelPath = prepModelFolder()
	with open(predFile,'w') as tsvfile:
		writer = csv.writer(tsvfile, delimiter='\t')
		for t_question in testQuestions:
			t_question['question'] = filterPunctuation(t_question['question'])
			corpus = []
			#print(len(t_question['comments']))
			for rel_comment in t_question['comments']:
				rel_comment['comment'] = filterPunctuation(rel_comment['comment'])
				corpus.append(dictionary.doc2bow(word_tokenize(rel_comment['comment'].lower())))
				# if(withStops):
				# 	comment = word_tokenize(rel_comment['comment'].lower())
				# else:
				# 	rel_comment['comment'] = ' '.join([i for i in t_question['question'] if i not in stops])
				# 	comment = word_tokenize(rel_comment['comment'].lower())
				# print(dictionary.doc2bow(comment))
				#corpus.append(dictionary.doc2bow(comment))
			if(len(corpus) > 1):
				lsi, index = generateLSIModel(corpus, dictionary, numFeatures)
			if(withStops):
				doc = word_tokenize(t_question['question'].lower())
			else:
				t_question['question'] = ' '.join([i for i in t_question['question'].lower() if i not in stops])
				doc = word_tokenize(t_question['question'].lower())
			vec_bow = dictionary.doc2bow(doc)
			vec_lsi = lsi[vec_bow]
			sims = index[vec_lsi]
			for idx, quest in enumerate(t_question['comments']):
				quest['simVal'] = sims[idx]
				writer.writerow([t_question['threadId'], quest['comment_id'], idx, quest['simVal'], quest['comment_rel']])




#createLSIPredictionFile(origQfilePath, SemDictionary, 100, False,'Sem')
#createLSIPredictionFile(origQfilePath, SemDictionary, 100, True, 'Sem')

createLSIPredictionFileSubTaskA(subtaskATestFilePath, SemDictionary, 100, False, 'Sem')
createLSIPredictionFileSubTaskA(subtaskATestFilePath, SemCDictionary, 100, True, 'SemC')




