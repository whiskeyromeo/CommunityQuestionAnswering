import json
import re
from pprint import pprint

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

#Andy : This should match the output of your loader from the FeatureDevelopment package. Hopefully it will be
# roughly plug and play...
#
#   Note: Some of the usernames came through as NULL in the crawler data so you may need to correct for this.
#
#   To test: Try it out on the questFileExample.json as the larger file will probably take a while.
def parseCrawlerData(filepath):
	questions = {}
	with open(filepath) as f:
		for line in f:
			question = {}
			data = json.loads(line)
			question['question'] = data['question'].replace(u'\xa0', u' ')
			question['subject'] = data['subject'].replace(u'\xa0', u' ')
			question['id'] = data['question_id']
			question['username'] = data['username']
			question['topic'] = data['topic']
			question['featureVector'] = []
			questions[data['question_id']] = question
			if('comments' in data):
				comments = {}
				for c in data['comments']:
					thisComment = {}
					thisComment['comment'] = c['comment'].replace(u'\xa0', u' ')
					thisComment['id'] = c['commentId']
					thisComment['username'] = c['username']
					thisComment['date'] = 'NULL'
					comments[c['commentId']] = thisComment
				questions[data['question_id']]['comments'] = comments 
					#comments[c['comment_id']['comment']] = c['comment'].replace(u'\xa0', u' ')
		return questions