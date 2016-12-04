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
        dictionary.head(10)
        dictionary=dictionary.set_index(['rqid'])
        output=pandas.DataFrame.join(output,dictionary)
        output.head(10)

        return output

    @staticmethod
    def getLsiDict():
        dictionary=pickle.read_pickle('..'+os.sep + "projectMidPoint" + os.sep + "tmp" + os.sep + "LsiModel" + os.sep + "mergeLsiData.dict")
        return dictionary