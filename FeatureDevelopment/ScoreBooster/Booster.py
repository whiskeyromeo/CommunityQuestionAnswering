import os

from gensim import *

print(os.path.dirname(os.path.abspath(__file__)))
dictionary = corpora.Dictionary.load("." + os.sep + "projectMidPoint"+os.sep+"tmp"+os.sep+"LsiModel"+os.sep+"LsiModel.dict")

pickle.unpickle()

print(dictionary)
