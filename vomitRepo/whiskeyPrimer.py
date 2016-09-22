"""XML parsing using the NLTK"""
__author__ = "whiskeyromeo"

import nltk, re, pprint
import xml.etree.ElementTree as ElementTree
import sys
import os
sys.path.append(os.path.abspath("../HTMLOutput"))
import HTMLOutput as HTMLOutput

output = HTMLOutput.HTMLOutput()

# from nltk.stem.porter import PorterStemmer

def getValues(tree, category):
    parent = tree.find(".//parent[@name='%s']" % category)
    return [child.get('value') for child in parent]

filePath = '../Data/train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-train-reformatted-excluding-2016-questions-cleansed.xml'



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

thisList = elementParser(filePath)
question_sents = []
question_words = []
pos_questions = []
question_bigrams = []



for row in thisList:
	print row
	# tokenize the questions into sentences
	sent_tokenized = nltk.sent_tokenize(row['question'])
	question_sents.append(sent_tokenized)

	# tokenize the questions into words
	word_tokenized = nltk.word_tokenize(row['question'])

	#Create a bigram distribution of the words from each question
	quest_bigram = nltk.bigrams(word_tokenized)
	question_bigrams.append(quest_bigram)

	#remove the stopwords from each sentence
	stopwords = nltk.corpus.stopwords.words('english')
	word_tokenized = [i for i in word_tokenized if i not in stopwords]
	question_words.append(word_tokenized)


	# tokenize the questions into words with part of speech tagging
	pos_tokenized = nltk.pos_tag(nltk.word_tokenize(row['question']))
	pos_questions.append(pos_tokenized)

# create an array of all of the words from all of the questions
flattened = []
for question in question_words:
	for word in question:
		flattened.append(word)
#### General Frequency Distribution ############


output.adddata("question_words", question_words)
output.adddata("flatted", flattened)

# Get the frequency distribution of all of the words across all the questions
word_dist = nltk.FreqDist(flattened)
# for word, freq in word_dist.most_common(50):
# 	print('{}: {}'.format(word, freq))

##### NGrams ###########

#compute frequency distribution for the bigrams found in the first question
fdist = nltk.FreqDist(question_bigrams[0])
# for k,v in fdist.items():
#     print k,v

#print question_sents[0]

# for value in question_bigrams[0]:
# 	print value

###### General iteration #######
# for row in question_sents:
	# print row
# for row in pos_questions:
# 	print row

# for row in question_words:
# 	print row

htmlpath = output.render()
print "Output is at " + htmlpath

