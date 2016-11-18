from utilities import *
import pandas
import xml.etree.ElementTree as ElementTree


class Merger:

    @staticmethod
    def merge(classificationsDataFrame):
        output = classificationsDataFrame.mean(axis=1)
        output = pandas.DataFrame(output)
        output.columns = ['Score']
        return output
