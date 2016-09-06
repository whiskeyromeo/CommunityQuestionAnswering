"""XML parsing using the NLTK"""
__author__ = "whiskeyromeo"

import nltk, re, pprint
import xml.etree.ElementTree as ElementTree

def getValues(tree, category):
    parent = tree.find(".//parent[@name='%s']" % category)
    return [child.get('value') for child in parent]

filePath = '../Data/train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-train-reformatted-excluding-2016-questions-cleansed.xml'



"""
Returns an array populated with questions
The comments are nested in each question

"""
def elementParser(filepath):
	tree = ElementTree.parse(filepath)
	root = tree.getroot()

	threadList = []
	for Thread in root.findall('Thread'):
		QuestionDict = {}
		relQuestion = Thread.find('RelQuestion')
		subject = relQuestion.find('RelQSubject').text
		#Pull the values from the questions into the relevant fields
		QuestionDict['threadId'] = relQuestion.attrib['RELQ_ID']
		QuestionDict['subject'] = subject
		QuestionDict['question'] = relQuestion.find('RelQBody').text
		comments = []
		# Pull the comments in
		for relComment in Thread.findall('RelComment'):
			commentDict = {}
			commentDict['comment'] = relComment.find('RelCText').text
			commentDict['comment_id'] = relComment.attrib['RELC_ID']
			comments.append(commentDict)
		# set the comments key to be equal to the question's comments
		QuestionDict['comments'] = comments
		#put the comments into the Question object
		threadList.append(QuestionDict)
	return threadList

thisList = elementParser(filePath)
for row in thisList:
	print row
