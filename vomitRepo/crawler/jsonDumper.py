import json
import re
from pprint import pprint

someList = []

def cleanLine():
	return

with open('questFile.json') as f:
	for line in f:
		data = json.loads(line)
		data['question'] = data['question'].replace(u'\xa0', u' ')
		data['subject'] = data['subject'].replace(u'\xa0', u' ')
		if('comments' in data):
			for c in data['comments']:
				c['comment'] = c['comment'].replace(u'\xa0', u' ')
		someList.append(data)

pprint(someList)