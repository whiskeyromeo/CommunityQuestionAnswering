import os
from pathlib import Path
import this
from pprint import pprint
from subprocess import call
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
        pprint(output[0:10])
        dictionary=Merger.getLsiDict()
        dictionary=pandas.DataFrame(dictionary)
        print("Data frame of incoming Lsi data: ")
        pprint(dictionary.head(10))
        dictionary=dictionary.set_index(['rqid'])
        output=pandas.DataFrame.join(output,dictionary)
        output["WeightedScore"]=((output["Score"])+(output["simval"]))
        print('\nJoined data frames on QID_RQID and counted lsi with twice weight of doc2vec:')
        pprint(output[0:10])
        return output

    @staticmethod
    def getLsiDict():
        externalFilePath = ".." + os.sep + "projectMidPoint" + os.sep + "tmp" + os.sep + "LsiModel" + os.sep + "mergeLsiData.dict"
        externalFile = Path(externalFilePath)
        if not externalFile.is_file():
            print("Running Will's LSI Model\n")
            os.chdir('..' + os.sep + '..' + os.sep + "projectMidPoint" + os.sep)
            call(["python", "LsiModel.py"])
        dictionary=pickle.read_pickle(externalFilePath)
        os.chdir('..' + os.sep + 'FinalProject' + os.sep + 'FeatureDevelopment')
        return dictionary
