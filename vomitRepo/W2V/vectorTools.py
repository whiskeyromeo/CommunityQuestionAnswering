from utils.QuestionFileCreator import QuestionCleaner
from utils.cosineSimilarity import cosineSimilarity
from nltk.corpus import stopwords
import numpy as np
import nltk

def buildQuestionMap(questionList):
	questions = QuestionCleaner(questionList)
	generateTokens(questions)
	model = buildBasicW2VModel(questions)
	generateAvgVectors(model, questions, 100)
	return questions



def generateTokens(questionList=[]):
	stops = set(stopwords.words('english'))
	for i,q in enumerate(questionList):
		split = nltk.word_tokenize(q['question'].lower())
		split = [w for w in split if w not in stops]
		q['question_tokens'] = split

def generateQuestionVector(model, question, numFeatures):
	featureVec = np.zeros((numFeatures,),dtype="float32")
	num_words = 0
	index2word_set = set(model.index2word)
	for word in question:
		if word in index2word_set: 
			num_words = num_words + 1
			featureVec = np.add(featureVec,model[word])
	featureVec = np.divide(featureVec,num_words)
	return featureVec

def generateAvgVectors(model, questionList, numFeatures):
	for q in questionList:
		q['question_vector'] = generateQuestionVector(model, q['question_tokens'], numFeatures)



def generateCosineSimilarities(testQuestion, questionList):
	questionVectors = []
	for q in questionList:
		questionVectors.append(q['question_vector'])
	sims = cosineSimilarity(testQuestion['question_vector'], questionVectors)
	for i,sim in enumerate(sims):
		questionList[i]['W2V_sim'] = sim
	return questionList 

