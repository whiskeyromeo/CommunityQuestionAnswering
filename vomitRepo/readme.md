##TO RUN

###Note : Must be run using python 2.7

<b>FROM data/english_scorer_and_random_baselines_v2.2</b>


###Doc2Vec

<p>So far we have 2 doc2vec versions, neither meets the baseline</p>

<b>To run script:</b>

```
	python doc2vec1.py
```

<b>To test</b>

```
	python ./MAP_scripts/ev.py SemEval2016-Task3-CQA-QL-dev.xml.subtaskB.relevancy ../../vomitRepo/SemEval2016-Task3-CQA-QL-dev-d2v-with-stops.pred
```
```
	python ./MAP_scripts/ev.py SemEval2016-Task3-CQA-QL-dev.xml.subtaskB.relevancy ../../vomitRepo/SemEval2016-Task3-CQA-QL-dev-d2v.pred
```

###LSI

<p>So far 1 LSI model, test is better than that of doc2vec, and with addition of more lines to the dictionary could potentially improve more.</p>

<p>Changed the number of features and had the exact same MAP average in all cases where features > 200. Stops didn't make a difference as they did in Doc2Vec</p>

<b>To run script:</b>

```
	python LsiModel.py
```

<b>To test</b>

```
	python ./MAP_scripts/ev.py SemEval2016-Task3-CQA-QL-dev.xml.subtaskB.relevancy ../../vomitRepo/SemEval2016-Task3-CQA-QL-dev-lsi400-with-stops.pred
	
```