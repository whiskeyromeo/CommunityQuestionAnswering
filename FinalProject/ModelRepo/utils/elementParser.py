'''
	__authors__ = Will Russell, Josh Ramer
'''
import xml.etree.ElementTree as ElementTree
import re
import json

def getValues(tree, category):
    parent = tree.find(".//parent[@name='%s']" % category)
    return [child.get('value') for child in parent]

"""
Returns an array populated with questions
The comments are nested in each question

"""
def elementParser(filepath):
	# construc the Element Tree and get the root
	tree = ElementTree.parse(filepath)
	root = tree.getroot()
	# create a list to store the pulled threads
	threadList = []
	# find each thread in the tree, starting at the root
	for Thread in root.findall('Thread'):
		# create a dict for each question
		QuestionDict = {}
		# find each question 
		relQuestion = Thread.find('RelQuestion')
		# pull the subject
		subject = relQuestion.find('RelQSubject').text
		#Pull the values from the questions into the relevant fields of the question dict
		QuestionDict['threadId'] = relQuestion.attrib['RELQ_ID']
		QuestionDict['subject'] = subject
		QuestionDict['question'] = relQuestion.find('RelQBody').text
		if(QuestionDict['question'] is None):
			QuestionDict['question'] = QuestionDict['subject']
		comments = []
		# Pull the comments from the filepath
		for relComment in Thread.findall('RelComment'):
			#create a dict for the comment
			commentDict = {}
			#populate the comment dict
			commentDict['comment'] = relComment.find('RelCText').text
			commentDict['comment_id'] = relComment.attrib['RELC_ID']
			relevancy = relComment.attrib['RELC_RELEVANCE2RELQ']
			if(relevancy == 'PerfectMatch' or relevancy == 'Good'):
				relevant = 'true'
			else:
				relevant = 'false'
			commentDict['comment_rel'] = relevant
			comments.append(commentDict)
		# set the comments key to be equal to the question's comments
		QuestionDict['comments'] = comments
		#put the comments into the Question object
		threadList.append(QuestionDict)
	return threadList

"""
	Takes a filePath and returns a List of original question objects
"""
def originalQuestionParser(filepath):
	tree = ElementTree.parse(filepath)
	root = tree.getroot()
	questList = []
	formerQuestionID = ''
	for origQuestion in root.findall('OrgQuestion'):	
		# find each original question
		currentQuestionID = origQuestion.attrib['ORGQ_ID']
		if(currentQuestionID != formerQuestionID):
			if('OrigQDict' in locals()):
				OrigQDict['rel_questions'] = relQuestions
				questList.append(OrigQDict)
			#Create a dict for the original questions
			OrigQDict = {}
			relQuestions = []
			OrigQDict['quest_ID'] = origQuestion.attrib['ORGQ_ID']
			OrigQDict['subject'] = origQuestion.find('OrgQSubject').text
			OrigQDict['origQuestion'] = origQuestion.find('OrgQBody').text
		relQuestion = {}
		Thread = origQuestion.find('Thread')
		relComments = []
		for comment in Thread.findall('RelComment'):
			relComments.append(findCommentForOrigQ(comment))
		relQuestion['comments'] = relComments
		RelQuestion = Thread.find('RelQuestion')
		relQuestion['rel_quest_ID'] = RelQuestion.attrib['RELQ_ID']
		relQuestion['category'] = RelQuestion.attrib['RELQ_CATEGORY']
		relQuestion['username'] = RelQuestion.attrib['RELQ_USERNAME']
		relQuestion['subject'] = RelQuestion.find('RelQSubject').text
		relQuestion['question'] = RelQuestion.find('RelQBody').text
		if(relQuestion['question'] is None):
			relQuestion['question'] = relQuestion['subject']
		relevancy = RelQuestion.attrib['RELQ_RELEVANCE2ORGQ']
		if(relevancy == 'PerfectMatch' or relevancy == 'Good'):
			relevant = 'true'
		else:
			relevant = 'false'
		relQuestion['relevant'] = relevant
		relQuestions.append(relQuestion)
		formerQuestionID = currentQuestionID
	return questList

'''
	Creates a list of hashes based on the crawler data
'''
def createObjectListFromJson(filepath):
	someList = []
	with open(filepath) as f:
		for line in f:
			data = json.loads(line)
			data['question'] = data['question'].replace(u'\xa0', u' ')
			data['subject'] = data['subject'].replace(u'\xa0', u' ')
			if('comments' in data):
				for c in data['comments']:
					c['comment'] = c['comment'].replace(u'\xa0', u' ')
			someList.append(data)
		return someList


'''
	This pulls out the relevant information for each comment for each thread in the
	original question file
'''
def findCommentForOrigQ(RelComment):
	relComment = {}
	relComment['rel_comment_ID'] = RelComment.attrib['RELC_ID']
	relComment['username'] = RelComment.attrib['RELC_USERNAME']
	relComment['comment'] = RelComment.find('RelCText').text
	relORGQ = RelComment.attrib['RELC_RELEVANCE2ORGQ']
	if(relORGQ == 'PerfectMatch' or relORGQ == 'Good'):
		relevant = 'true'
	else:
		relevant = 'false'
	relComment['relORGQ'] = relevant
	relRELQ = RelComment.attrib['RELC_RELEVANCE2RELQ']
	if(relRELQ == 'PerfectMatch' or relRELQ == 'Good'):
		relevant = 'true'
	else:
		relevant = 'false'
	relComment['relRELQ'] = relevant
	return relComment
