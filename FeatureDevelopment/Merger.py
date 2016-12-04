import os
import this

from pandas.io import pickle

from utilities import *
import pandas
from gensim import *


class Merger:

    @staticmethod
    def merge(classificationsDataFrame):
        output = classificationsDataFrame.mean(axis=1)
        output = pandas.DataFrame(output)
        output.columns = ['Score']
        dictionary=Merger.getLsiDict()
        return output,dictionary

    @staticmethod
    def getLsiDict():
        dictionary=pickle.read_pickle('..'+os.sep + "projectMidPoint" + os.sep + "tmp" + os.sep + "LsiModel" + os.sep + "mergeLsiData.dict")
        return dictionary