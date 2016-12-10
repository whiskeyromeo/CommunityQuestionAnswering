import os
import glob

os.chdir('./models')
filenames = []
for file in glob.glob('*.pred'):
	filenames.append(file)

os.chdir('..')
for file in filenames:
	os.system("gnome-terminal -e 'bash -c \"python .scorer/MAP_scripts/ev.py SemEval2016-Task3-CQA-QL-dev.xml.subtaskB.relevancy ./models/" + file +";exec bash\"'")


os.system("gnome-terminal -e 'bash -c \"sl; exec bash\"'")

