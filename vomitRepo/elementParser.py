
import xml.etree.ElementTree as ElementTree


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
		RelQuestion = Thread.find('RelQuestion')
		relQuestion['rel_quest_ID'] = RelQuestion.attrib['RELQ_ID']
		relQuestion['category'] = RelQuestion.attrib['RELQ_CATEGORY']
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




