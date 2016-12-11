'''
 __author__ = Will Russell

'''


class DataParser:
	

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


	'''

	'''
	def QTLQuestionCreator(filePaths=[]):
		questionList = []
		for filePath in filePaths:
			questionList += createObjectListFromJson(filePath)
		return questionList

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



	'''

	'''
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


	'''

	'''
	def getQuestionsFromQTL(hashlist):
		questions = []
		for row in hashlist:
			qData = {
				"id": row["question_id"],
				"question":row["question"]
			}
			questions.append(qData)
		return questions


	'''

	'''
	def getCommentsFromQTL(hashlist):
		comments = []
		for row in hashlist:
			if 'comments' in row:
				for c in row['comments']:
					cData = {
						"id": c['commentId'],
						"question": c['comment']
					}
					comments.append(cData)
		return comments

	'''

	'''
	def combineDocumentData(task3HashList, QTLHashList, comments=False):
		docs = DataParser.getQuestions(task3HashList)
		docs += DataParser.getQuestionsFromQTL(QTLHashList)
		if(comments):
			docs += DataParser.getComments(task3HashList)
			docs += DataParser.getCommentsFromQTL(QTLHashList)
		return docs