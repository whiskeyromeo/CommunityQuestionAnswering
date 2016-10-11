## SemEval Task 3 - Community Question Answering - Subtask B
**Contributors**
* Andy Fabian
* Emily Klein
* Josh Ramer
* Will Russell

***

##Overview
As part of the SemEval Competition we chose to pursue SubTask B, Question-to-Question ranking which involved attempting to develop a ranking system which would return the 10 most relevant questions when compared to a given question. 

In order to achieve this we have used two different methods so far, Latent Semantic Analysis, and Paragraph2Vec using cosine similarity. Both implementations have been performed using the gensim python library.
***

###


##Example output
<p>Below are examples of the required input for compiling the python code and the resulting output when tested against the MAP scorer</p>

<h3>Using Doc2Vec</h3>
<p>Terminal input to compile the python file and run the associated scripts contained within: </p>
```
	python doc2vec1.py
```
<p>Terminal input to Use the scorer:</p>
<p>With stopwords : </p>
```
	python ./MAP_scripts/ev.py SemEval2016-Task3-CQA-QL-dev.xml.subtaskB.relevancy ../../vomitRepo/SemEval2016-Task3-CQA-QL-dev-d2v-with-stops.pred
```
<p>Without stopwords: </p>
```
	python ./MAP_scripts/ev.py SemEval2016-Task3-CQA-QL-dev.xml.subtaskB.relevancy ../../vomitRepo/SemEval2016-Task3-CQA-QL-dev-d2v.pred
```
<p>Example Terminal Output of Doc2Vec with stopwords: </p>

```
*** Official score (MAP for SYS): 0.5634


******************************
*** Classification results ***
******************************

Acc = 0.6939
P   = 1.0000
R   = 0.2788
F1  = 0.4361


********************************
*** Detailed ranking results ***
********************************

IR  -- Score for the output of the IR system (baseline).
SYS -- Score for the output of the tested system.

           IR   SYS
MAP   : 0.7101 0.5634
AvgRec: 0.8601 0.7393
MRR   :  76.19  63.35
              IR    SYS              IR    SYS              IR    SYS            IR  SYS
REC-1@01:  69.39  51.02  ACC@01:  69.39  51.02  AC1@01:   0.81   0.60  AC2@01:   34   25
REC-1@02:  81.63  67.35  ACC@02:  68.37  45.92  AC1@02:   0.83   0.56  AC2@02:   67   45
REC-1@03:  81.63  73.47  ACC@03:  61.90  44.90  AC1@03:   0.81   0.59  AC2@03:   91   66
REC-1@04:  81.63  73.47  ACC@04:  56.63  45.92  AC1@04:   0.80   0.65  AC2@04:  111   90
REC-1@05:  81.63  81.63  ACC@05:  53.88  47.76  AC1@05:   0.80   0.71  AC2@05:  132  117
REC-1@06:  85.71  81.63  ACC@06:  51.36  44.90  AC1@06:   0.83   0.72  AC2@06:  151  132
REC-1@07:  85.71  83.67  ACC@07:  49.27  44.61  AC1@07:   0.88   0.79  AC2@07:  169  153
REC-1@08:  85.71  83.67  ACC@08:  46.17  43.88  AC1@08:   0.90   0.86  AC2@08:  181  172
REC-1@09:  85.71  83.67  ACC@09:  44.22  43.08  AC1@09:   0.95   0.92  AC2@09:  195  190
REC-1@10:  85.71  85.71  ACC@10:  42.45  42.45  AC1@10:   1.00   1.00  AC2@10:  208  208

REC-1 - percentage of questions with at least 1 correct answer in the top @X positions (useful for tasks where questions have at most one correct answer)
ACC   - accuracy, i.e., number of correct answers retrieved at rank @X normalized by the rank and the total number of questions
AC1   - the number of correct answers at @X normalized by the number of maximum possible answers (perfect re-ranker)
AC2   - the absolute number of correct answers at @X

```




clear introduction to problem,
point by point outline of solution,
and examples of actual program input and output