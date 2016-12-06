import os
import this
from pprint import pprint

from pandas.io import pickle

from utilities import *
import pandas
from gensim import *


class Merger:

    @staticmethod
    def merge(classificationsDataFrame):
        output = classificationsDataFrame.mean(axis=1)
        output = pandas.DataFrame(output)
        output.columns=['Score']
        dictionary=Merger.getLsiDict()
        dictionary=pandas.DataFrame(dictionary)
        print("Data frame of incoming Lsi data: ")
        pprint(dictionary.head(10))
        dictionary=dictionary.set_index(['rqid'])
        output=pandas.DataFrame.join(output,dictionary)
        output["Score"]=((output["Score"])+(output["simval"]))
        print('\nJoined data frames on QID_RQID and counted lsi with twice weight of doc2vec:')
        # output=output.__delitem__('')
        pprint(output[0:10])
        return output

    @staticmethod
    def getLsiDict():
        dictionary=pickle.read_pickle('..'+os.sep + "projectMidPoint" + os.sep + "tmp" + os.sep + "LsiModel" + os.sep + "mergeLsiData.dict")
        return dictionary