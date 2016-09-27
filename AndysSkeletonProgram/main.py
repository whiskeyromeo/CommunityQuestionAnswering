import sys
import webbrowser
sys.path.append('../HTMLOutput/')
from HTMLOutput import HTMLOutput
from loader import loadXMLQuestions
from preprocessSentencesAndWords import *
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

# arguments:
#   --setup - do any 1-time setup necessary, such as downloading dictionaries
#   --nobrowser - don't open a web browser with the output file
#   --nostopwords - don't remove stopwords from the input
#   --questionfile=file.xml - file containing the question/answer XML data

##############################################################################################

# Start up output system

global output
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

# Pre-process:
# - augment questions and answers with versions of those split into sentences
# - create bigram distributions of the words from each question
# - remove stopwords
# - part-of-speech tagging

print("PreProcessing: Sentences and Words")
QAData = preprocessAddSentencesAndWords(QAData)
output.adddata("Sentences", QAData[0:2])

if "--nostopwords" not in sys.argv:
    print("PreProcessing: Stopwords")
    QAData = preprocessStopwords(QAData)
    output.adddata("Stopwords: stopwords", preprocessStopwordsList())
    output.adddata("Stopwords", QAData[0:2])

print("PreProcessing: Bigrams")
QAData = preprocessBigram(QAData)
output.adddata("Bigram", QAData[0:2])

print("PreProcessing: Parts of Speech")
QAData = preprocessPartOfSpeech(QAData)
output.adddata("PartOfSpeech", QAData[0:2])

# Transform data into feature sets

if "--doc2vec" in sys.argv:
    print("Feature Generation: Doc2Vec")
    QAData = featuresdoc2vec(QAData)
    output.adddata("Doc2Vec", QAData[0:2])

# Run/train the comparison system

# Final output

print("Output: Rendering HTML")
outputpath = output.render()
print("Output: rendered to " + outputpath)

if "--nobrowser" not in sys.argv:
    print("Output: Launching browser")
    webbrowser.open(outputpath)

print("Finished")