from whiskeyPrimer2 import elementParser
import os
import re
import logging
logging.basicConfig(filename='./logs/QuestionFileCreator.log', format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def QuestionCreator(filePaths):
	thisList = []
	questions = []
	for filePath in filePaths:
		thisList += elementParser(filePath)
	for row in thisList:
		questions.append(row['question'])
	return questions

def QuestionFileCreator(filename, questions):
	file = open(filename, 'w')
	logging.info('Ready to write to ' + filename)
	for row in questions:
		re.sub('[\s+]',' ', 'row')
		file.write(row + '\n')
	logging.info('Finished writing to ' + filename)


'''
	Params: filename : a string representing the desired 
	directory/filename

	Returns : a string representing the destination file to save various 
	formats to with name consistency
'''
def CreateFilePath(filename):
	folder_path = './tmp/' + filename
	if not os.path.exists(folder_path):
		os.makedirs(folder_path)
	new_dest = folder_path + '/' + filename
	return new_dest 