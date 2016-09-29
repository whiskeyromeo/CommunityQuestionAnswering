import sys
import webbrowser
sys.path.append('../HTMLOutput/')
from HTMLOutput import HTMLOutput
from loader import loadXMLQuestions
from preprocessWords import *
from preprocessBigram import *
from preprocessStopwords import *
from preprocessPartOfSpeech import *
from featuresDoc2Vec import *
from setup import setup
from pprint import pprint

def getargvalue(name, required):
    output = False
    for arg in sys.argv:
        if arg[2:len(name)+2] == name:
            output = arg[3+len(name):]
    if required and not output:
        raise Exception("Required argument " + name + " not found in sys.argv")
    return output

# Question-to-Question Module
#
# Task: train or compute how similar two questions are to each other

# arguments:
#   --setup - do any 1-time setup necessary, such as downloading dictionaries
#   --nobrowser - don't open a web browser with the output file
#   --nostopwords - don't remove stopwords from the input
#   --questionfile=file.xml - file containing the question/answer XML data

##############################################################################################

# Start up output system

output = HTMLOutput()
output.adddata("Command Line", sys.argv)

# One-time setup

if "--setup" in sys.argv:
    setup()

# Load data from files

print("Loading")
questionFile = getargvalue("questionfile", True)
QAData = loadXMLQuestions(questionFile)
output.adddata("Loader", QAData)

# Pre-process: takes in question and outputs additional attributes, such as question_words

print("PreProcessing: Words")
QAData = preprocessAddWords(QAData, output)
output.adddata("Words", QAData[0:2])

if "--nostopwords" not in sys.argv:
    print("PreProcessing: Stopwords")
    QAData = preprocessStopwords(QAData, output)
    output.adddata("Stopwords: stopwords", preprocessStopwordsList())
    output.adddata("Stopwords", QAData[0:2])

print("PreProcessing: Bigrams")
QAData = preprocessBigram(QAData, output)
output.adddata("Bigram", QAData[0:2])

print("PreProcessing: Parts of Speech")
QAData = preprocessPartOfSpeech(QAData, output)
output.adddata("PartOfSpeech", QAData[0:2])

# Feature generation: takes question_words or other question attributes, outputs question_features_*

if "--doc2vec" in sys.argv:
    print("Feature Generation: Doc2Vec")
    QAData = featuresdoc2vec(QAData, output)
    output.adddata("Doc2Vec", QAData[0:2])

# TODO: Other feature generators

# TODO: Merge all features into final feature set

# Run/train the comparison system (iterate over each pair of questions)

# TODO:

# Final output (sort scores)

# TODO: Output in correct format for scoring system

print("Output: Rendering HTML")
outputpath = output.render()
print("Output: rendered to " + outputpath)

if "--nobrowser" not in sys.argv:
    print("Output: Launching browser")
    webbrowser.open(outputpath)

print("Finished")