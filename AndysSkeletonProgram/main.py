import sys
import webbrowser
sys.path.append('../HTMLOutput/')
from HTMLOutput import HTMLOutput
from loader import loadXMLQuestions
from preprocessSentencesAndWords import *
from preprocessBigram import *
from preprocessStopwords import *
from preprocessPartOfSpeech import *
from setup import setup

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

output = HTMLOutput()
output.adddata("Command Line", sys.argv)

# One-time setup

if "--setup" in sys.argv:
    setup()

# Load data from files

questionFile = getargvalue("questionfile", True)
QAData = loadXMLQuestions(questionFile)
output.adddata("Loader: questionList", QAData)

# Pre-process:
# - augment questions and answers with versions of those split into sentences
# - create bigram distributions of the words from each question
# - remove stopwords
# - part-of-speech tagging

QAData = preprocessAddSentencesAndWords(QAData)
output.adddata("Sentences: questionList", QAData)

if "--nostopwords" not in sys.argv:
    QAData = preprocessStopwords(QAData)
    output.adddata("Stopwords: stopwords", preprocessStopwordsList())
    output.adddata("Stopwords: questionList", QAData)

QAData = preprocessBigram(QAData)
output.adddata("Bigram: questionList", QAData)

QAData = preprocessPartOfSpeech(QAData)
output.adddata("PartOfSpeech: questionList", QAData)

# Transform data into feature sets

# Run/train the comparison system

# Final output

outputpath = output.render()
print("Output rendered to " + outputpath)

if "--nobrowser" not in sys.argv:
    webbrowser.open(outputpath)
