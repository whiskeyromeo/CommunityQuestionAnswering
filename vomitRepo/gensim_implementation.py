from whiskeyPrimer2 import elementParser, filePaths
from collections import defaultdict
from gensim import corpora, models, similarities
from six import iteritems
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

thisList = []
# Create the list full of all of the data
for filePath in filePaths:
	thisList += elementParser(filePath)

# Create a list to hold all of the questions
questions = []
for row in thisList:
	questions.append(row['question'])

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

#dictionary.save('./tmp/firstQueries.dict')
#
# Create a vector representation of the questions, Using same format as 
# what went into the dictionary so that we can properly map ids/values
corpus = [dictionary.doc2bow(query) for query in queries]
#

# Save corpus as Matrix Market file

#corpora.MmCorpus.serialize('./tmp/firstQueries.mm', corpus)

# or SVMlight format, Blei LDA-C, GibbsLDA++

#corpora.SvmLightCorpus.serialize('./tmp/corpus.svmlight', corpus)
#corpora.BleiCorpus.serialize('./tmp/corpus.lda-c', corpus)
#corpora.LowCorpus.serialize('./tmp/corpus.low', corpus)



######################
# Memory Friendly Implementation
######################

# Open up a new file to write to

#f = open('myfile.txt','w')

# Remove whitespace and newlines from the question text and write each question
# to a single line in a file

# for row in questions:
# 	re.sub('[\s+]', ' ', row)
# 	f.write(row + "\n")

stops = set('for a of the and to in'.split())
# collect stats about all tokens
dictionary = corpora.Dictionary(line.lower().split() for line in open('myfile.txt'))
# remove stopwords
stop_ids = [dictionary.token2id[stopword] for stopword in stops if stopword in dictionary.token2id]
# remove words only appearing once
once_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq == 1]
dictionary.filter_tokens(stop_ids + once_ids)
dictionary.compactify()

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
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)
corpus_lsi = lsi[corpus_tfidf]

# Save the model to disk for later
lsi.save('./tmp/model.lsi')
lsi = models.LsiModel.load('./tmp/model.lsi')

##########################
# Queries with cosine similarities
#########################

# Need to enter all documents which need comparison against subsequent queries
# !!NOTE!!: 
#	Running MatricSimilarity with a large set of documents( >= 1,000,000) coupled with a large
#	number of features will hog a lot of RAM(1M @ 256 feature_count = >2GB RAM)
# 	If RAM is an issue, use similarities.Similarity 
index = similarities.MatrixSimilarity(lsi[corpus])
# index.save('./tmp/firstQueries.index')
# index = similarities.MatrixSimilarity.load('./tmp/firstQueries.index')

# Perform a similarity query against the corpus( returns a bunch of 2-tuples)
sims = index[vec_lsi]

# sort the result
sims = sorted(enumerate(sims), key=lambda item: -item[1])

for key, value in sims[:10]:
	print key
	print questions[key]
	print value
	print "************"






