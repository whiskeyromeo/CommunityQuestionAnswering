"""
This was the best system tested
"""

from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from nltk.corpus import stopwords
from QuestionFileCreator import getQuestions, getComments, QuestionCleaner
from sourceFiles import thisList, origQfilePath
from doc2vec1 import createPredictionFile

stops = set(stopwords.words('english'))

"""
	Takes in a list of Questions and outputs a list of TaggedDocument objects
	Params:
		questions: a list of questions
		withStops: A boolean value representing whether to remove stops or not
	Returns:
		mod_questions: A list of TaggedDocument objects which consists of a list of words
			for each document and associated tags for each word

"""
def prepLabeledSentList(questions = [], withStops = False):
	mod_questions = []
	for q in questions:
		if(withStops):
			mod_questions.append(TaggedDocument([i for i in q['question'] if i not in stops], q['id']))
		else:
			mod_questions.append(TaggedDocument(q['question'], q['id']))
	return mod_questions


"""
	prepModel takes in a list of TaggedDocuments and parameters to be passed into 
	the creation of the Doc2Vec object and outputs a prepared Doc2Vec model
	Params:
		mod_questions : a list of TaggedDocuments
		size : The number of features to be used in the Doc2Vec model
		window : The window size
		minCount : The minimum count of each word to be taken into account in the model creation
		workers : Number of worker threads to use in creation of the model
"""
def prepModel(mod_questions, size=100, window=5, minCount=5, workers=4):
	model = Doc2Vec(mod_questions, size=size, window=window, min_count=minCount, workers=workers)
	model_name = 'doc2vec_size{}window{}min{}work{}'.format(size, window, minCount, workers)
	model.save('./tmp/'+ model_name)
	return model

questions = getQuestions(thisList)
#questions += getComments(thisList)
mod_questions = prepLabeledSentList(questions, True)
model = prepModel(mod_questions)


# Prep the predictive models
createPredictionFile(origQfilePath, model)
createPredictionFile(origQfilePath, model, False)

