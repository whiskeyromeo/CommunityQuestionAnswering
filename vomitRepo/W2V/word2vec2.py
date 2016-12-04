from nltk.corpus import stopwords
import gensim
from gensim import utils
from gensim.models import Word2Vec
import numpy as np
from random import shuffle
from pprint import pprint
import csv
import re
import logging
import numpy
import os
import sys
import pickle
import nltk
from pathlib import Path 

from vectorTools import *

#Generate the dimensions for the word2vec model
DIM = 600
TOKEN_LIMIT = 30000
WORKERS = 8
WINDOW = 10
DYNAMIC_WINDOW = False
NEGATIVE = 10

'''
	Need to generate a set of functions which can create a model based on the vocabulary derived from both the crawler json files and the xml files
'''

from word2vec1 import questions, qtlQuestions

questionList = []
for q in questions:
	questionList.append(q['question_tokens'])
id2word = gensim.corpora.Dictionary(questionList)
word2id = dict((v,k) for k,v in id2word.iteritems())
corpus = lambda: ([word.lower() for word in question if word in word2id] for question in questionList)

# This seems to be the ideal sampling method based on the gensim team comparison
model = Word2Vec(size=DIM, window=WINDOW, workers=WORKERS,hs=0,negative=NEGATIVE)
model.build_vocab(corpus())
model.train(corpus())


