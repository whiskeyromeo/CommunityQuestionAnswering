##TO RUN

###Note : Must be run using python 2.7

<b>FROM data/english_scorer_and_random_baselines_v2.2</b>

<p>So far we have 2 versions, neither meets the baseline</p>
```
	python ./MAP_scripts/ev.py SemEval2016-Task3-CQA-QL-dev.xml.subtaskB.relevancy ../../vomitRepo/SemEval2016-Task3-CQA-QL-dev-with-stops.pred
```
```
	python ./MAP_scripts/ev.py SemEval2016-Task3-CQA-QL-dev.xml.subtaskB.relevancy ../../vomitRepo/SemEval2016-Task3-CQA-QL-dev.pred
```