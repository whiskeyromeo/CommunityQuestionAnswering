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
		QuestionDict['threadId'] = relQuestion.attrib['RELQ_ID']
		QuestionDict['subject'] = subject
		QuestionDict['question'] = relQuestion.find('RelQBody').text
		comments = {}
		for relComment in Thread.findall('RelComment'):
			comments['comment'] = relComment.find('RelCText').text
			comments['comment_id'] = relComment.attrib['RELC_ID']
		QuestionDict['comments'] = comments
		threadList.append(QuestionDict)
	return threadList

thisList = elementParser(filePath)
for row in thisList:
	print row