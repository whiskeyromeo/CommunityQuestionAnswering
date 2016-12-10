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
print('''
			This file will execute the MAP scorer on the .pred files
			contained within the models folder. To proceed through 
			the files, please press enter on this console window 
			when you are ready to view the next set of results. 


			Getting ready to run experiments....



			Here we go....



	''')
os.chdir('..')
for file in filenames:
	print('###################################')
	print('Running MAP for :' + file)
	print('Press enter when ready')
	if 'subtaskA' in file:
		os.system("gnome-terminal -e 'bash -c \"python ./scorer/MAP_scripts/ev.py ./scorer/SemEval2016-Task3-CQA-QL-dev-subtaskA.xml.subtaskA.relevancy ./models/" + file +";exec bash\"'")
		raw_input()
	else:
		os.system("gnome-terminal -e 'bash -c \"python ./scorer/MAP_scripts/ev.py ./scorer/SemEval2016-Task3-CQA-QL-dev.xml.subtaskB.relevancy ./models/" + file +";exec bash\"'")
		raw_input()
os.system("gnome-terminal -e 'bash -c \"sl; exec bash\"'")
print('All prediction files executed. Have a nice day.')