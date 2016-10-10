from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from nltk.corpus import stopwords

from QuestionFileCreator import getQuestions, getComments, QuestionCleaner
from sourceFiles import thisList


stops = set(stopwords.words('english'))


def prepLabeledSentList(questions = [], withStops = False):
	mod_questions = []
	for q in questions:
		#print('idx: ' + str(idx) + ' , question: ' + question)
		mod_questions.append(TaggedDocument([i for i in q['question'] if i not in stops], q['id']))
	return mod_questions


def prepModel(mod_questions, size=100, window=8, minCount=5, workers=4):
	model = Doc2Vec(mod_questions, size=size, window=window, min_count=minCount, workers=workers)
	model_name = 'doc2vec_size{}window{}min{}work{}'.format(size, window, minCount, workers)
	model.save('./tmp/'+ model_name)
	return model

questions = getQuestions(thisList)
mod_questions = prepLabeledSentList(questions)
model = prepModel(mod_questions)


# def altDoc2Vec(questions):
# 	mod_questions = prepLabeledSentList(questions)
# 	model = Doc2Vec(min_count=1, window=10, size=100, sample=1e-4, negative=5, workers=8)
# 	model.build_vocab(mod_questions)
# 	shuffle(mod_questions)

# 	for epoch in range(10):
# 		model.train(mod_questions)

# 	model.save('./tmp/doc2vec_size100window10min5work4samp1e-4')
# 	return model