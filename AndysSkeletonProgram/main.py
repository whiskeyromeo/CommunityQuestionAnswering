import sys
import webbrowser
sys.path.append('../HTMLOutput/')
from HTMLOutput import HTMLOutput

# Start up output system

output = HTMLOutput()

# Load data from files

output.addstring("test page", "this is a test")
output.addstring("test page", "this is another test")

# Pre-process data to normalize text and remove junk

# Transform data into feature sets

# Run/train the comparison system

# Final output

outputpath = output.render()
print "Output rendered to", outputpath
webbrowser.open(outputpath)