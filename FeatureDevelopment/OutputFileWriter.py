from utilities import *
import csv
import pandas
import xml.etree.ElementTree as ElementTree


class OutputFileWriter:

    @staticmethod
    def write(outputDataFrame, outputFilename, questions):
        output = OutputFileWriter.getSorted(outputDataFrame)
        with open(outputFilename, "w") as tsvfile:
            writer = csv.writer(tsvfile, delimiter="\t")
            for id, values in output.iterrows():
                score = values['WeightedScore']
                qid = id.split('_')[0]
                question = questions[qid]['related'][id]
                if question['givenRelevance'] == 'PerfectMatch' or question['givenRelevance'] == 'Relevant':
                    relevance = 'true'
                else:
                    relevance = 'false'
                writer.writerow([qid, id, 0, score, relevance])

    @staticmethod
    def getSorted(dataframe):
        sortkeys = pandas.Series(name='sortkey')
        for k, v in dataframe.iterrows():
            sortkeys[k] = OutputFileWriter.getkey(k)
        dataframe['sortkey'] = sortkeys
        return dataframe.sort_values('sortkey')

    @staticmethod
    def getkey(k):
        qvalue = k.split('_')[0][1:]
        rvalue = k.split('_')[1][1:]
        newvalue = int(qvalue) * 1000 + int(rvalue)
        return newvalue