__author__ = 'Will Russell'

from utils.elementParser import elementParser, createObjectListFromJson
from pathlib import Path 
import pickle
import os
import sys




origQfilePath = '../../Data/english_scorer_and_random_baselines_v2.2/SemEval2016-Task3-CQA-QL-dev.xml'
subtaskATestFilePath = '../../Data/english_scorer_and_random_baselines_v2.2/SemEval2016-Task3-CQA-QL-dev-subtaskA.xml'

filePaths = [
	'../../Data/train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-train-reformatted-excluding-2016-questions-cleansed.xml',
	'../../Data/train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-dev-reformatted-excluding-2016-questions-cleansed.xml',
	'../../Data/train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-test-reformatted-excluding-2016-questions-cleansed.xml',
	'../../Data/train/SemEval2016-Task3-CQA-QL-train-part2-subtaskA.xml',
	'../../Data/train/SemEval2016-Task3-CQA-QL-train-part1-subtaskA.xml'
]


filePathsSubTaskA = [
	'../../Data/train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-train-reformatted-excluding-2016-questions-cleansed.xml',
	'../../Data/train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-dev-reformatted-excluding-2016-questions-cleansed.xml',
	'../../Data/train/SemEval2016-Task3-CQA-QL-train-part2-subtaskA.xml',
	'../../Data/train/SemEval2016-Task3-CQA-QL-train-part1-subtaskA.xml'
]

QTLfilePaths = [
	'../../Data/QTLCrawlerData/questFile.json',
	'../../Data/QTLCrawlerData/questFile2.json',
	'../../Data/QTLCrawlerData/questFile3.json',
	'../../Data/QTLCrawlerData/questFile4.json'
]


if(Path("../tmp/QTL_list.p").is_file()):
	QTL_List = pickle.load(open("../tmp/QTL_List.p", "rb"))
else:
	QTL_List = []
	for filePath in QTLfilePaths:
		QTL_List += createObjectListFromJson(filePath)
	if not os.path.isdir('../tmp'):
		os.makedirs('../tmp')
	pickle.dump(QTL_List, open("../tmp/QTL_List.p", "wb"))


if(Path("../tmp/thisList.p").is_file()):
	thisList = pickle.load(open("../tmp/thisList.p", "rb"))
else:
	thisList = []
	for filePath in filePaths:
		thisList += elementParser(filePath)
	if not os.path.isdir('../tmp'):
		os.makedirs('../tmp')
	pickle.dump(thisList, open("../tmp/thisList.p", "wb"))

if(Path("../tmp/subTaskAList.p").is_file()):
	subTaskAList = pickle.load(open("../tmp/subTaskAList.p", "rb"))
else:
	subTaskAList = []
	for filePath in filePathsSubTaskA:
		subTaskAList += elementParser(filePath)
	if not os.path.isdir('../tmp'):
		os.makedirs('../tmp')
	pickle.dump(subTaskAList, open("../tmp/subTaskAList.p", "wb"))
