'''
	Execution of this file will run all of the 
'''

import os
import glob

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
		os.system("gnome-terminal -e 'bash -c \"python -c \'print(\'OUTPUT FROM "+ file +"\')\'; python ./scorer/MAP_scripts/ev.py ./scorer/SemEval2016-Task3-CQA-QL-dev-subtaskA.xml.subtaskA.relevancy ./models/" + file +";exec bash\"'")
	else:
		os.system("gnome-terminal -e 'bash -c \"python -c \'print(\'OUTPUT FROM "+ file +"\')\'; python ./scorer/MAP_scripts/ev.py ./scorer/SemEval2016-Task3-CQA-QL-dev.xml.subtaskB.relevancy ./models/" + file +";exec bash\"'")


os.system("gnome-terminal -e 'bash -c \"sl; exec bash\"'")

