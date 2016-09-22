import sys
import webbrowser
sys.path.append('../HTMLOutput/')
from HTMLOutput import HTMLOutput
from loader import loadXMLQuestions

# Start up output system

output = HTMLOutput()

# Load data from files

questionList = loadXMLQuestions('../Data/train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-train-reformatted-excluding-2016-questions-cleansed.xml')
output.adddata("Loader: questionList", questionList)

# Pre-process data to normalize text and remove junk

# Transform data into feature sets

# Run/train the comparison system

# Final output

outputpath = output.render()
print "Output rendered to", outputpath

if "--nobrowser" not in sys.argv:
    webbrowser.open(outputpath)
