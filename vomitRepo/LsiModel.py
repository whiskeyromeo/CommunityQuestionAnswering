from gensim import corpora, models, similarities
from six import iteritems
from QuestionFileCreator import CreateFilePath, getQuestions, QuestionCleaner
from elementParser import originalQuestionParser
from whiskeyPrimer2 import thisList
from nltk.corpus import stopwords
import logging
import os
import re
import csv

#For Saving the lsi model for later
new_dest = CreateFilePath('LsiModel')

logging.basicConfig(filename=new_dest +'.log', format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

stops = set(stopwords.words('english'))

questions = QuestionCleaner(getQuestions(thisList))


# Dictionary is generated based on the question content of thisList
dictionary = corpora.Dictionary(line['question'].lower().split() for line in questions)
# remove stopwords
stop_ids = [dictionary.token2id[stopword] for stopword in stops if stopword in dictionary.token2id]
# remove words only appearing once
once_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq == 1]
dictionary.filter_tokens(stop_ids + once_ids)
dictionary.compactify()
dictionary.save(new_dest +'.dict')


def generateLSIModel(corpus, dictionary, numTopics):
	corpora.MmCorpus.serialize(new_dest + '.mm', corpus)
	serialized_corpus = corpora.MmCorpus(new_dest + '.mm')
	tfidf = models.TfidfModel(corpus)
	corpus_tfidf = tfidf[corpus]
	lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=numTopics)
	index = similarities.MatrixSimilarity(lsi[serialized_corpus])
	return lsi, index

origQfilePath = '../Data/english_scorer_and_random_baselines_v2.2/SemEval2016-Task3-CQA-QL-dev.xml'

def createLSIPredictionFile(filePath, dictionary, numFeatures=200, withStops=True):
	testQuestions = originalQuestionParser(filePath)
	head, tail = os.path.split(filePath)
	tail = tail.split('.')[0]
	if(withStops):
		predFile = tail +'-lsi' + str(numFeatures) +'-with-stops.pred'
	else:
		predFile = tail + '-lsi' + str(numFeatures) + '.pred'
	for oq in testQuestions:
		oq['origQuestion'] = re.sub('[^\w\s]', ' ', oq['origQuestion'])
		oq['origQuestion'] = re.sub('[\s+]', ' ', oq['origQuestion'])
		for q in oq['rel_questions']:
			q['question'] = re.sub('[^\w\s]', ' ', q['question'])
			q['question'] = re.sub('[\s+]', ' ', q['question'])
	with open(predFile, 'w') as tsvfile:
		writer = csv.writer(tsvfile, delimiter='\t')
		for t_question in testQuestions:
			corpus = [dictionary.doc2bow(q['question'].lower().split()) for q in t_question['rel_questions']]
			lsi, index = generateLSIModel(corpus, dictionary, numFeatures)
			if(withStops):
				doc = t_question['origQuestion']
			else: 
				t_question['origQNoStops'] = " ".join([i for i in t_question['origQuestion'].lower().split() if i not in stops])
				doc = t_question['origQNoStops']
			vec_bow = dictionary.doc2bow(doc.lower().split())
			vec_lsi = lsi[vec_bow]
			sims = index[vec_lsi]
			for idx, quest in enumerate(t_question['rel_questions']):
				quest['simVal'] = sims[idx]
				writer.writerow([t_question['quest_ID'], quest['rel_quest_ID'], idx, quest['simVal'], quest['relevant']])

createLSIPredictionFile(origQfilePath, dictionary, 400)


