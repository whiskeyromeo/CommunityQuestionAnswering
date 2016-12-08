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
from utils.QuestionFileCreator import CreateFilePath, filterPunctuation, prepModelFolder, initializeLog
from utils.elementParser import elementParser, originalQuestionParser
from utils.sourceFiles import thisList, QTL_List, subTaskAList, origQfilePath, subtaskATestFilePath
from utils.DataParser import DataParser as DP

initializeLog()

stops = set(stopwords.words('english'))

if not os.path.isdir('tmp'):
	os.makedirs('tmp')

def generateDictionaries():
	# Create dictionary based on SemEval Questions
	if(Path("./tmp/LSIModel-Sem").is_file()):
		print('SemEval Question Dictionary Found')
		SemDictionary = dictionary.load('./LSIModel-Sem.dict')
	else:
		print('Creating SemEval Dictionary...')
		sources = filterPunctuation(DP.getQuestions(thisList))
		SemDictionary = createDictionary(sources, 'Sem')

	# Create Dictionary based on SemEval Question + Comments
	if(Path("./tmp/LSIModel-SemC").is_file()):
		print('SemEval Question/Comment Dictionary Found')
		SemCDictionary = dictionary.load('./LSIModel-SemC.dict')
	else:
		print('Creating SemEval Question/Comment Dictionary...')
		sources = filterPunctuation(DP.getQuestions(thisList))
		sources += filterPunctuation(DP.getComments(thisList))
		SemCDictionary = createDictionary(sources, 'SemC')

	# Create Dictionary based on SemEval Questions + Crawler Questions
	if(Path("./tmp/LSIModel-QTL").is_file()):
		print('QatarLiving + SemEval Dictionary Found')
		QTLDictionary = dictionary.load('./LSIModel-QTL.dict')
	else:
		print('Creating QatarLiving + SemEval Question Dictionary...')
		sources = filterPunctuation(DP.combineDocumentData(thisList, QTL_List))
		QTLDictionary = createDictionary(sources, 'QTL')

	# Create Dictionary based on SemEval Questions+Comments and Crawler Question+Comments
	if(Path("./tmp/LSIModel-QTLC").is_file()):
		print('QatarLiving + SemEval Question/Comment Dictionary Found')
		QTLCDictionary = dictionary.load('./LSIModel-QTLC.dict')
	else:
		print('Creating QatarLiving + SemEval Question/Comment Dictionary...')
		sources = filterPunctuation(DP.combineDocumentData(thisList, QTL_List, True))
		QTLCDictionary = createDictionary(sources, 'QTLC')
	return SemDictionary, SemCDictionary, QTLDictionary, QTLCDictionary


SemDictionary, SemCDictionary, QTLDictionary, QTLCDictionary = generateDictionaries()


def createDictionary(sources, fileName="LSIModel", fileTag=''):
	dictionary = corpora.Dictionary(line['question'].lower().word_tokenize() for line in sources)
	stop_ids = [dictionary.token2id[stopword] for stopword in stops if stopword in dictionary.token2id]
	once_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq == 1]
	dictionary.filter_tokens(stop_ids + once_ids)
	dictionary.compactify()
	if(len(fileTag) > 0):
		fileTag = '-' + fileTag
	filename = fileName + fileTag + '.dict'
	dictionary.save('tmp/' + filename)
	return dictionary



def generateLSIModel(corpus, dictionary, numTopics):
	corpora.MmCorpus.serialize('LSIModel.mm', corpus)
	serialized_corpus = corpora.MmCorpus('LSIModel.mm')
	tfidf = models.TfidfModel(corpus)
	corpus_tfidf = tfidf[corpus]
	lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=numTopics)
	index = similarities.MatrixSimilarity(lsi[serialized_corpus])
	return lsi, index



def createLSIPredictionFile(filePath, dictionary, numFeatures=200, withStops=True):
	testQuestions = originalQuestionParser(filePath)
	head, tail = os.path.split(filePath)
	tail = tail.split('.')[0]
	if(withStops):
		predFile = tail +'-lsi' + str(numFeatures) +'-with-stops.pred'
	else:
		predFile = tail + '-lsi' + str(numFeatures) + '.pred'
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
			lsi, index = generateLSIModel(corpus, dictionary, numFeatures)
			if(withStops):
				doc = t_question['origQuestion']
			else: 
				t_question['origQNoStops'] = " ".join([i for i in t_question['origQuestion'].lower().word_tokenize() if i not in stops])
				doc = t_question['origQNoStops']
			vec_bow = dictionary.doc2bow(doc.lower().word_tokenize())
			vec_lsi = lsi[vec_bow]
			sims = index[vec_lsi]
			for idx, quest in enumerate(t_question['rel_questions']):
				quest['simVal'] = sims[idx]
				writer.writerow([t_question['quest_ID'], quest['rel_quest_ID'], idx, quest['simVal'], quest['relevant']])


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
			for rel_comment in t_question['comments']:
				rel_comment['comment'] = filterPunctuation(rel_comment['comment'])
				corpus.append(dictionary.doc2bow(doc.lower().word_tokenize()))
			lsi, index = generateLSIModel(corpus, dictionary, numFeatures)
			if(withStops):
				doc = t_question['question']
			else:
				t_question['question'] = ' '.join([i for i in t_question['question'] if i not in stops])
				doc = t_question['question']
			vec_bow = dictionary.doc2bow(doc.lower().word_tokenize())
			vec_lsi = lsi[vec_bow]
			sims = index[vec_lsi]
			for idx, quest in enumerate(t_question['comments']):
				quest['simVal'] = sims[idx]
				writer.writerow([t_question['threadId'], row['comment_id'], 0, row['simVal'], row['comment_rel']])




createLSIPredictionFile(origQfilePath, SemDictionary, 100, False,'Sem')
createLSIPredictionFile(origQfilePath, SemDictionary, 100, True, 'Sem')

createLSIPredictionFileSubTaskA(subtaskATestFilePath, SemCDictionary, 100, False, 'SemC')
createLSIPredictionFileSubTaskA(subtaskATestFilePath, SemCDictionary, 100, True, 'SemC')




