from gensim import corpora, models, similarities
from six import iteritems
from nltk.corpus import stopwords
import logging
import os
import sys

sys.path.insert(0, os.path.abspath('..'))
from utils.QuestionFileCreator import CreateFilePath, getQuestions, QuestionCleaner, initializeLog
from utils.sourceFiles import thisList

initializeLog()

new_dest = CreateFilePath('LsiModel')


stops = set(stopwords.words('english'))

questions = QuestionCleaner(getQuestions(thisList))

dictionary = corpora.Dictionary(line['question'].lower().split() for line in questions)
# remove stopwords
stop_ids = [dictionary.token2id[stopword] for stopword in stops if stopword in dictionary.token2id]
# remove words only appearing once
once_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq == 1]
dictionary.filter_tokens(stop_ids + once_ids)
dictionary.compactify()
dictionary.save(new_dest +'.dict')


class MyCorpus(object):
	def __iter__(self):
		for line in questions:
			yield dictionary.doc2bow(line['question'].lower().split())

corpus = MyCorpus()

corpora.MmCorpus.serialize(new_dest +'.mm', corpus)

serialized_corpus = corpora.MmCorpus(new_dest + '.mm')

tfidf = models.TfidfModel(corpus) 
corpus_tfidf = tfidf[corpus]


lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=200)
corpus_lsi = lsi[corpus_tfidf]

index = similarities.MatrixSimilarity(lsi[serialized_corpus])

doc = questions[0]['question']
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_lsi = lsi[vec_bow]
sims = index[vec_lsi]




#Sort the sims according to those most like the original question
#sims = sorted(enumerate(sims), key=lambda item: -item[1])

# for key, value in sims[:10]:
# 	print(key)
# 	print(questions[key])
# 	print(value)
# 	print("************")