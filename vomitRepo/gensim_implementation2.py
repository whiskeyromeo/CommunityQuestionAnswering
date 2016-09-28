from whiskeyPrimer2 import filePaths
from collections import defaultdict
from gensim import corpora, models, similarities
from six import iteritems
import logging
from QuestionFileCreator import CreateFilePath, QuestionCreator

# Create the uniform filepath for saving documents
new_dest = CreateFilePath('genImp2')


logging.basicConfig(filename=new_dest +'.log', format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

# Create a list to hold all of the questions
questions = QuestionCreator(filePaths)
# get the stopwords
stops = set('for a of the and to in'.split())

# remove the stopwords, tokenize the questions
queries = [[word for word in question.lower().split() if word not in stops] for question in questions]


# remove words that appear only once
frequency = defaultdict(int)
for query in queries:
	for token in query:
		frequency[token] += 1


# Create a dictionary to represent the words by their mapped integer ids
# Access representations via dictionary.token2id
dictionary = corpora.Dictionary(queries)

dictionary.save(new_dest +'.dict')
#
# Create a vector representation of the questions, Using same format as 
# what went into the dictionary so that we can properly map ids/values
corpus = [dictionary.doc2bow(query) for query in queries]
#

# Save corpus as Matrix Market file

corpora.MmCorpus.serialize(new_dest +'.mm', corpus)

# or SVMlight format, Blei LDA-C, GibbsLDA++

#corpora.SvmLightCorpus.serialize(new_dest +'.svmlight', corpus)
#corpora.BleiCorpus.serialize(new_dest +'.lda-c', corpus)
#corpora.LowCorpus.serialize(new_dest +'.low', corpus)




#########################
# Implementing a Transformation
#########################

# Initialize a weighted model
tfidf = models.TfidfModel(corpus) 

# Apply transformation to an entire corpus
corpus_tfidf = tfidf[corpus]
	# for doc in corpus_tfidf:
	# 	print doc

# Initialize an LSI transformation(Latent Semantic Indexing)
# Transform the weighted tfidf corpus into latent 2-d space(num_topics = dimensions)
# num_topics should be between 200-500 as that has found to be the sweet spot...
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=200)
corpus_lsi = lsi[corpus_tfidf]

# Save the model to disk for later
lsi.save(new_dest +'.lsi')
lsi = models.LsiModel.load(new_dest +'.lsi')

##########################
# Queries with cosine similarities
#########################

# Need to enter all documents which need comparison against subsequent queries
# !!NOTE!!: 
#	Running MatricSimilarity with a large set of documents( >= 1,000,000) coupled with a large
#	number of features will hog a lot of RAM(1M @ 256 feature_count = >2GB RAM)
# 	If RAM is an issue, use similarities.Similarity 

index = similarities.MatrixSimilarity(lsi[corpus])

index.save(new_dest +'.index')
index = similarities.MatrixSimilarity.load(new_dest +'.index')



# Perform a similarity query against the corpus( returns a bunch of 2-tuples)
doc = questions[0]
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_lsi = lsi[vec_bow] # convert the query to LSI space
sims = index[vec_lsi]

# sort the result
sims = sorted(enumerate(sims), key=lambda item: -item[1])

for key, value in sims[1:10]:
	print key
	print questions[key]
	print value
	print "************"


