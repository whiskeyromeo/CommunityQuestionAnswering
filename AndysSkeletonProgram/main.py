import sys
import webbrowser
sys.path.append('../HTMLOutput/')
from HTMLOutput import HTMLOutput
from loader import loadXMLQuestions

def getargvalue(name, required):
    output = False
    for arg in sys.argv:
        if arg[2:len(name)+2] == name:
            output = arg[3+len(name):]
    if required and not output:
        raise Exception("Required argument " + name + " not found in sys.argv")
    return output

# arguments:
#   --nobrowser - don't open a web browser with the output file
#   --questionfile=file.xml - file containing the question/answer XML data

# Start up output system

output = HTMLOutput()
output.adddata("Command Line", sys.argv)

# Load data from files

questionFile = getargvalue("questionfile", True)
questionList = loadXMLQuestions(questionFile)
output.adddata("Loader: questionList", questionList)

# Pre-process data to normalize text and remove junk

# Transform data into feature sets

# Run/train the comparison system

# Final output

outputpath = output.render()
print("Output rendered to " + outputpath)

if "--nobrowser" not in sys.argv:
    webbrowser.open(outputpath)
