"""
	This file takes in the documents to be used in the training set
	and outputs a list containing hashes populated with information
	relevant to each question
"""

from elementParser import elementParser

filePaths = [
	'../Data/train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-train-reformatted-excluding-2016-questions-cleansed.xml',
	'../Data/train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-dev-reformatted-excluding-2016-questions-cleansed.xml',
	'../Data/train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-test-reformatted-excluding-2016-questions-cleansed.xml',
	#'../Data/dev/SemEval2016-Task3-CQA-QL-dev-subtaskA.xml',
	'../Data/train/SemEval2016-Task3-CQA-QL-train-part2-subtaskA.xml',
	'../Data/train/SemEval2016-Task3-CQA-QL-train-part1-subtaskA.xml'
]

thisList = []

for filePath in filePaths:
	thisList += elementParser(filePath)


origQfilePath = '../Data/english_scorer_and_random_baselines_v2.2/SemEval2016-Task3-CQA-QL-dev.xml'
