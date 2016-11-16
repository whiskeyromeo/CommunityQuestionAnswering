
from gensim.models import word2vec

import numpy as np
import pandas as pd
from sklearn import naive_bayes, svm, preprocessing
from sklearn.decomposition import TruncatedSVD

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_selection.univariate_selection import chi2, SelectKBest

from nltk.corpus import stopwords
stops = stopwords.words('english')

from utils.QuestionFileCreator import QuestionCleaner, getQuestions, getComments
from utils.sourceFiles import thisList, origQfilePath
from utils.elementParser import originalQuestionParser
from D2V.doc2vec3 import model

questions = QuestionCleaner(getQuestions(thisList))
questions += QuestionCleaner(getComments(thisList))

questionList = []
for q in questions:
	q['question'] = [w for w in q['question'].lower().split() if not w in stops]
	questionList.append(q['question'])

vectorizer = CountVectorizer(analyzer='word', \
							 tokenizer=None, \
							 preprocessor=None, \
							 stop_words=None, \
							 max_features=5000)

train_data_features = vectorizer.fit_transform(questionList)
train_data_features = train_data_features.toarray()

# Get a list of all words from the feature list
vocab = vectorizer.get_feature_names()
# Sum the counts for each vocab word
dist = np.sum(train_data_features, axis=0)

num_features = 300
min_word_count = 30
num_workers = 4
context = 10
downsampling = 1e-3

model = word2vec.Word2Vec(questionList, workers=num_workers, \
					size=num_features, min_count=min_word_count, \
					window=context, sample=downsampling)

# No more training, makes the model more memory friendly
model.init_sims(replace=True)


def makeFeatureVec(words, model, num_features):
	#preallocation of numpy array for speed purposes
	featureVec = np.zeros((num_features,), dtype="float32")
	nwords = 0
	#Convert model vocabulary to set for speed
	index2word_set = set(model.index2word)
	for word in words:
		if word in index2word_set:
			nwords = nwords+1
			featureVec = np.add(featureVec, model[word])
	print("nwords = " + str(nwords))
	featureVec = np.divide(featureVec, nwords)
	return featureVec

# def getAvgFeatureVecs(questions, model, num_features):
# 	counter = 0
# 	#preallocation of numpy array for speed purposes
# 	reviewFeatureVecs = np.zeros((len(questions), num_features), dtype="float32")
# 	for question in questions:
# 		reviewFeatureVecs[counter] = makeFeatureVec(question, model, num_features)
# 		counter += 1
# 	return questionFeatureVecs


# TODO: Figure out how to implement tfidf weighting against
# the word2vec vectors

testQuestions = originalQuestionParser(origQfilePath)  

for t_quest in testQuestions:
	t_quest['wordList'] = t_quest['origQuestion'].lower().split()
	t_quest['w2vectors'] = makeFeatureVec(t_quest['wordList'], model, num_features)
	for rel_quest in t_quest['rel_questions']:
		rel_quest['wordList'] = rel_quest['question'].lower().split()
		rel_quest['w2vectors'] = makeFeatureVec(rel_quest['wordList'], model, num_features)



# def createW2VPredictionFile(filePath, model, withStops=True):
# 	testQuestions = originalQuestionParser(filePath)
# 	head, tail = os.path.split(filePath)
# 	tail = tail.split('.')[0]
# 	if(withStops):
# 		predFile = tail + '-w2v-with-stops.pred'
# 	else:
# 		predFile = tail + '-w2v.pred'
# 	with open(predFile, "w") as tsvfile:
# 		writer = csv.writer(tsvfile, delimiter="\t")
# 		for t_question in testQuestions:
# 			if(withStops):
# 				t_question['wordArray'] = t_question['origQuestion'].lower().split()
# 			else: 
# 				t_question['wordArray'] = [i for i in t_question['origQuestion'].lower().split() if i not in stops]
# 			#
# 			for rel_quest in t_question['rel_questions']:
# 				if(withStops):
# 					rel_quest['wordArray'] = rel_quest['question'].lower().split()
# 				else:
# 					rel_quest['wordArray'] = [i for i in rel_quest['question'].lower().split() if i not in stops]
# 				rel_quest['WMDistance'] = model.wmdistance(t_question['wordArray'], rel_quest['wordArray'])	
# 				writer.writerow([t_question['quest_ID'], row['rel_quest_ID'], 0, row['WMDistance'], row['relevant']])
				
#createW2VPredictionFile(origQfilePath, model)
