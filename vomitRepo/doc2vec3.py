from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from nltk.corpus import stopwords
from QuestionFileCreator import getQuestions, getComments, QuestionCleaner
from sourceFiles import thisList, origQfilePath
from doc2vec1 import createPredictionFile

stops = set(stopwords.words('english'))

def prepLabeledSentList(questions = [], withStops = False):
	mod_questions = []
	for q in questions:
		mod_questions.append(TaggedDocument([i for i in q['question'] if i not in stops], q['id']))
	return mod_questions


def prepModel(mod_questions, size=100, window=8, minCount=5, workers=4):
	model = Doc2Vec(mod_questions, size=size, window=window, min_count=minCount, workers=workers)
	model_name = 'doc2vec_size{}window{}min{}work{}'.format(size, window, minCount, workers)
	model.save('./tmp/'+ model_name)
	return model

questions = getQuestions(thisList)
#questions += getComments(thisList)
mod_questions = prepLabeledSentList(questions)
model = prepModel(mod_questions)

createPredictionFile(origQfilePath, model)
