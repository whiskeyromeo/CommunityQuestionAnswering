'''
	Execution of this file will run all of the prediction files in the models directory

	__author__= Will Russell
'''

import os
import glob
import zipfile

os.chdir('./models')
filenames = []
for file in glob.glob('*.pred'):
	filenames.append(file)

print('###################################')
print('Getting Ready to run experiments')
print('here we go...')
print('###################################')

os.chdir('..')
for file in filenames:
	if 'subtaskA' in file:
		os.system("gnome-terminal -e 'bash -c \"python ./scorer/MAP_scripts/ev.py SemEval2016-Task3-CQA-QL-dev-subtaskA.xml.subtaskA.relevancy ./models/" + file +";exec bash\"'")
	else:
		os.system("gnome-terminal -e 'bash -c \"python ./scorer/MAP_scripts/ev.py SemEval2016-Task3-CQA-QL-dev.xml.subtaskB.relevancy ./models/" + file +";exec bash\"'")


os.system("gnome-terminal -e 'bash -c \"sudo apt-get install sl, sl; exec bash\"'")

rootPath = './Data/'
