from utils.elementParser import elementParser
from pathlib import Path 
import pickle
import os

filePaths = [
	'../../Data/train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-train-reformatted-excluding-2016-questions-cleansed.xml',
	'../../Data/train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-dev-reformatted-excluding-2016-questions-cleansed.xml',
	'../../Data/train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-test-reformatted-excluding-2016-questions-cleansed.xml',
	#'../../Data/dev/SemEval2016-Task3-CQA-QL-dev-subtaskA.xml',
	'../../Data/train/SemEval2016-Task3-CQA-QL-train-part2-subtaskA.xml',
	'../../Data/train/SemEval2016-Task3-CQA-QL-train-part1-subtaskA.xml'
]

if(Path("./tmp/thisList.p").is_file()):
	thisList = pickle.load(open("tmp/thisList.p", "rb"))
else:
	thisList = []
	for filePath in filePaths:
		thisList += elementParser(filePath)
	if not os.path.exists(os.path.dirname('tmp')):
		os.makedirs('tmp')
	pickle.dump(thisList, open("tmp/thisList.p", "wb"))

origQfilePath = '../../Data/english_scorer_and_random_baselines_v2.2/SemEval2016-Task3-CQA-QL-dev.xml'

