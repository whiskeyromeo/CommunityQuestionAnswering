'''
	__author__ = Will Russell
'''

import sys
import os
import re
import logging

from utils.elementParser import elementParser
from crawler.jsonDumper import createObjectListFromJson

#Create the log for each time the compile goes down
def initializeLog():
	try:
		os.makedirs('logs')
	except OSError as e:
		if e.errno != 17:
			raise
		pass
	logging.basicConfig(filename='./logs/QuestionFileCreator.log', format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
	logger = logging.getLogger(__name__)


'''
	QuestionCreator takes an array of filepaths and uses them to construct an
	array of questions out of the object array created via the elementParser
	Returns : a populated array of questions
'''
def QuestionCreator(filePaths = []):
	thisList = []
	questions = []
	for filePath in filePaths:
		thisList += elementParser(filePath)
	for row in thisList:
		questions.append(row['question'])
	return questions


def QTLQuestionCreator(filePaths=[]):
	questionList = []
	for filePath in filePaths:
		questionList += createObjectListFromJson(filePath)
	return questionList


'''
	QuestionFileReader takes the name of a file which is comprised of questions
	and passes the file line by line into an array
	Returns :  the populated array of questions
'''
def QuestionFileReader(filename):
	questions = []
	file = open(filename, 'r')
	for line in file:
		questions.append(line)
	return questions

'''
	QuestionFileCreator takes a desired filename and and array of questions and creates
	a textfile based on those questions, while removing whitespace and logging to 
	a logfile
'''
def QuestionFileCreator(filename, questions=[]):
	file = open(filename + '.txt', 'w')
	logging.info('Ready to write to ' + filename)
	for row in questions:
		re.sub('[\s+]',' ', 'row')
		file.write(row + '\n')
	logging.info('Finished writing to ' + filename)

def prepModelFolder():
	cwd = os.getcwd()
	cwd = cwd.split('/')
	n = len(cwd)
	if(cwd[n-1].lower() == 'vomitrepo'):
		modelPath = './models/'
	else:
		modelPath = '../models/'
	try:
		os.makedirs(modelPath)
	except OSError as e:
		if e.errno != 17:
			raise
		pass
	return modelPath


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

'''
	Looks for particular traits in questions and removes the 
	questions if they have/don't have those particular traits

'''
def QuestionCleaner(questions = []):
	for q in questions:
		q['question'] = re.sub('[^\w\s]', ' ', q['question'])
		q['question'] = re.sub('[\s+]', ' ', q['question'])
	return questions

'''
	Removes all punctuation from a given sentence
'''
def filterPunctuation(sentence):
	sentence = re.sub('[^\w\s]', ' ', sentence)
	sentence = re.sub('[\s+]', ' ', sentence)
	return sentence


'''
	Takes a string to be used for the name of a textfile and a list of questions
	Creates a file based on the list of questions with each one of the questions
	being on a single row. 
'''
def CleanQuestionFileCreator(filename, questions):
	# Get over the damned 'ascii' cannot compile error...
	questions = QuestionCleaner(questions)
	reload(sys)
	file = open(filename + '.txt' , 'w')
	logging.info('Ready to write to cleanfile ' + filename)
	for idx, row in enumerate(questions):
		if idx == len(questions)-1:
			file.write(row)
		else:
			file.write(row + '\n')
	logging.info('Finished writing to cleanfile ' + filename)
	reload(sys)
	sys.setdefaultencoding('ascii')


'''
	Creates a list of hashes out of the questions and threadIds from the elementParser hash output
'''
def getQuestions(hashlist):
	questions = []
	for row in hashlist:
		qData = {
			"id": row["threadId"],
			"question": row["question"] 
		}
		questions.append(qData)
	return questions


def getComments(hashlist):
	comments = []
	for row in hashlist:
		for comment in row['comments']:	
			cData = {
				"id": comment["comment_id"],
				"question": comment["comment"]
			}
			comments.append(cData)
	return comments


def getQuestionsFromQTL(hashlist):
	questions = []
	for row in hashlist:
		qData = {
			"id": row["question_id"],
			"question":row["question"]
		}
		questions.append(qData)
	return questions

def getCommentsFromQTL(hashlist):
	comments = []
	for row in hashlist:
		if 'comments' in row:
			for c in row['comments']:
				cData = {
					"id": c['id'],
					"comment": c['comment']
				}
				comments.append(cData)
	return comments



