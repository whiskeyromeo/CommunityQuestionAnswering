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

###Introduction
> Community forums are increasingly gaining popularity as a way to pose questions and receive
> honest and open answers.  These forums are rarely moderated, allowing anyone to ask or respond to a question.
> The lack of moderation has many advantages including letting users post anything they want, resulting in
> some well thought out responses.  However, this openness comes with a downfall of people posting
> responses that are not relevant to the question asked.  Ranking comments that are most relevant to the question
> asked will save the user from sifting through hundreds of responses.  Further, providing a list of similar
> questions will provide the user with a bank of comments that could possibly provide they answer they are
> seeking.
>
>	The data in Semeval Task 3 comes from Qatar Living.  This is a forum where users can post questions about
> life in Qatar, and receive responses from the community.  We are focused on subtasks A and B, which is
> question-comment similarity and question-question similarity.  During this first stage, we have primarily
> focused on question-question similarity.  Our goals for the next stage of the project are to improve the
> accuracy of the question-question similarity, as well as work on question-comment similarity.

###Method
>  <b>SubTask B: Stage 1</b>
> 
> In order to determine related questions, we first created a term frequency-inverse document
> frequency matrix, where the questions were columns and vocabulary were rows.  We then
> performed latent semantic indexing on this matrix and then calculated the cosine similarity
> from the resulting matrix.  This allowed us to rank which questions were most similar to a given question.
> We tried using both Doc2Vec as well as LSI on the matrix created by TF-IDF.  We found that using LSI
> gave us slightly better results than Doc2Vec.  Finally, the Cosine Similarity was calculated on the vectors
> found using LSI, which gave us scores corresponding to the vectors.  From these scores, we were able to
> determine which questions ranked most similar to a question.
> 
> <b>SubTask B: Stage 2</b>
>
> We expanded on our original method mentioned above by incorporating new features by which to enhance our
> previous results. In addition, we developed a secondary method for document vector generation by averaging
> word2vec vectors of individual words in a given question. Though the method of vector averaging did not enhance our 
> results in SubTask B, it was more successful than the Doc2Vec models in Subtask A, though the source of the disparity
> in the results is something we are
> still investigating.
> 
> We were able to get a slight boost in the results from LSI obtained from Stage 1 through our FeatureDevelopment
> module.
> 
> <b>SubTask A: Stage 2</b>
>
>    We followed much of the same line of though in the approach to Subtask A as we did in Subtask B, which 
> the exception that we incorporated data pulled from the QatarLiving site via a webCrawler and also developed 
> a model based on averaging of word vectors obtained using Word2Vec to establish document vectors. This was found
> to provide better results than when using Doc2Vec in this task, however this did not carry over to Subtask B. We
> were not able to employ LSI on this subtask as there is a bug in the code for applying the LSI model
> which we have not yet been able to sort out. 
> 
>



###Tasks
From the SemEval Site:
> Our main CQA task, as in 2016, is:
> “given (i) a new question and (ii) a large collection of question-answer threads created by a user community, rank the 
> answer posts that are most useful for answering the new question.”

> Additionally, we propose two sub-tasks:

> [1] Question Similarity (QS): given the new question and a set of related questions from the collection, rank the similar 
> questions according to their similarity to the original question (with the idea that the answers to the similar
> questions should be answering the new question as well).

> [2] Relevance Classification (RC): given a question from a question-answer thread, rank the answer posts according to 
> their relevance with respect to the question.

***

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

###Resources
* [Gensim Topic Modelling Library](https://radimrehurek.com/gensim/)
* [SemanticZ from SemEval 2016 Task 3](http://www.aclweb.org/anthology/S/S16/S16-1136.pdf)
* [SemEval-2016 Task 3 Description Paper](http://alt.qcri.org/semeval2016/task3/data/uploads/semeval2016-task3-report.pdf)
* [Our github](https://github.com/whiskeyromeo/CommunityQuestionAnswering)