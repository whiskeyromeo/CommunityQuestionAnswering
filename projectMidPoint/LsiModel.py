"""
	This file performs Latent Semantic Indexing
	on a list of questions and outputs a prediction 
	file based on that indexing

	__author__ = Will Russell

"""

from gensim import corpora, models, similarities
from six import iteritems
from QuestionFileCreator import CreateFilePath, getQuestions, getComments, QuestionCleaner
from elementParser import elementParser, originalQuestionParser
from nltk.corpus import stopwords
import logging
import os
import re
import csv

from sourceFiles import thisList, origQfilePath

#For Saving the lsi model for later
new_dest = CreateFilePath('LsiModel')

logging.basicConfig(filename=new_dest +'.log', format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

stops = set(stopwords.words('english'))

sources = QuestionCleaner(getQuestions(thisList))
#sources += QuestionCleaner(getComments(thisList))

# Dictionary is generated based on the question content of thisList
dictionary = corpora.Dictionary(line['question'].lower().split() for line in sources)
# remove stopwords
stop_ids = [dictionary.token2id[stopword] for stopword in stops if stopword in dictionary.token2id]
# remove words only appearing once
once_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq == 1]
# Filter out stopwords and words which only occur once from the dictionary
dictionary.filter_tokens(stop_ids + once_ids)
dictionary.compactify()
dictionary.save(new_dest +'.dict')


"""
	Generates an LSI Model based on a prepared corpus and dictionary
	Params:
		corpus : A corpus of documents represented as a stream of vectors
		dictionary : A collection of word counts and relevant statistics for each word from the
			training set
		numTopics : Represents the dimensionality of LSI space to be used
	Returns:
		lsi: An lsi space generated from the corpus and dictionary
		index: An index of documents in LSI space to be compared against
"""
def generateLSIModel(corpus, dictionary, numTopics):
	corpora.MmCorpus.serialize(new_dest + '.mm', corpus)
	serialized_corpus = corpora.MmCorpus(new_dest + '.mm')
	# Apply tfidf weighting to the corpus
	tfidf = models.TfidfModel(corpus)
	corpus_tfidf = tfidf[corpus]
	# generate an lsi model based on the tfidf weighted corpus
	lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=numTopics)
	# Transform the corpus to LSI space and index it
	index = similarities.MatrixSimilarity(lsi[serialized_corpus])
	return lsi, index

"""
	createLSIPredictionFile outputs a prediction file based on
		a LSI model generated from a given dictionary 
	Params: 
		filePath: the filePath of the source to derive the prediction from
		dictionary: the dictionary to be used in the creation of the model
		numFeatures: The dimensionality of the 

"""
def createLSIPredictionFile(filePath, dictionary, numFeatures=200, withStops=True):
	testQuestions = originalQuestionParser(filePath)
	head, tail = os.path.split(filePath)
	tail = tail.split('.')[0]
	if(withStops):
		predFile = tail +'-lsi' + str(numFeatures) +'-with-stops.pred'
	else:
		predFile = tail + '-lsi' + str(numFeatures) + '.pred'
	for oq in testQuestions:
		# Remove all Punctuation, replacing it with a space
		oq['origQuestion'] = re.sub('[^\w\s]', ' ', oq['origQuestion'])
		# Remove all excess whitespace
		oq['origQuestion'] = re.sub('[\s+]', ' ', oq['origQuestion'])
		for q in oq['rel_questions']:
			q['question'] = re.sub('[^\w\s]', ' ', q['question'])
			q['question'] = re.sub('[\s+]', ' ', q['question'])
	with open(predFile, 'w') as tsvfile:
		writer = csv.writer(tsvfile, delimiter='\t')
		for t_question in testQuestions:
			# generate the corpus from a distributed bag of words representation based on the dictinonary
			corpus = [dictionary.doc2bow(q['question'].lower().split()) for q in t_question['rel_questions']]
			lsi, index = generateLSIModel(corpus, dictionary, numFeatures)
			# either keep or remove the stopwords based on the withStops boolean
			if(withStops):
				doc = t_question['origQuestion']
			else: 
				t_question['origQNoStops'] = " ".join([i for i in t_question['origQuestion'].lower().split() if i not in stops])
				doc = t_question['origQNoStops']
			# convert the vectors to a distributed bag of words representation
			vec_bow = dictionary.doc2bow(doc.lower().split())
			# convert the query to lsi space
			vec_lsi = lsi[vec_bow]
			# Perform a similarity query against the corpus for each question to rank against
			sims = index[vec_lsi]
			for idx, quest in enumerate(t_question['rel_questions']):
				# Perform a similarity query against the corpus for each question to be ranked
				quest['simVal'] = sims[idx]
				# Write out the values
				writer.writerow([t_question['quest_ID'], quest['rel_quest_ID'], idx, quest['simVal'], quest['relevant']])

# Create the LSI prediction files
createLSIPredictionFile(origQfilePath, dictionary, 400, False)
createLSIPredictionFile(origQfilePath, dictionary, 400)


