==============================================================
CQA-QL English corpus for SemEval-2016 Task 3
"Community Question Answering"
Version 3.2: December 25, 2015
==============================================================

This file contains the basic information regarding the CQA-QL English corpus provided for the SemEval-2016 task "Community Question Answering". The current version (3.2, December 25, 2015) corresponds to the release of the English training data set. The test sets will be provided in future versions. All changes and updates on these data sets are reported in Section 1 of this document.


[1] LIST OF VERSIONS

  v3.2 [2015/12/25]: added a version of the 2016 data for subtask A that includes an uncleansed multi-line version of the questions and of the comments;
                     added a cleansed version of the 2015 data;
                     added large unannotated data (189,941 questions and 1,894,456 comments, excluding those with annotations)

  v3.1 [2015/12/15]: added a version of the reformatted 2015 data
                     where the questions already present in 2016 are excluded;
                     fixed a typo in the DTD for the 2015 data

  v3.0 [2015/11/30]: added more training data;
                     XML validation added at the beginning of each XML file;
                     provided a reliable, double-checked DEV dataset;
                     added RELC_RELEVANCE2RELQ annotations for all parts of the dataset (no more "N/A");
                     added uncleansed, multi-line version of the text of the questions and of the comments;
                     added annotation about which threads are repeated (as repetitions are to be filtered for subtask A);
                     also added a version of the data where the repetitions of RelQuestions are removed (as an alternative data format for subtask A);
                     added the data from SemEval-2015 Task 3, reformatted and augmented with extra attributues (usable as extra training data for subtask A);
                     TOTAL DATA AVAILABLE:
                       - Subtask A (6,398 questions + 40,288 comments)
                       - Subtask B (317 original + 3,169 related questions)
                       - Subtask C (317 original questions + 3,169 related questions + 31,690 comments)

  v2.0 [2015/10/04]: added further training data, in a separate file (-part2):
                     100 more original questions, 1,000 related questions, 10,000 comments; unlike the previous distributions, this time there is judgments of relevance for each comment with respect to the related question (in addition to the relevance with respect to the original question)

  v1.1 [2015/09/05]: added more training data compared to the initial distribution:
                     103 original questions, 613 related questions, 5855 comments

  v1.0 [2015/09/01]: initial distribution of the English TRAINING data:
                     50 original questions, 500 related questions, 5000 comments


[2] CONTENTS OF THE DISTRIBUTION 3.1

We provide the following files:


* MAIN files

  * README.txt 
    this file

  * train/SemEval2016-Task3-CQA-QL-train-part1.xml
    first part of the TRAIN dataset consisting of 200 original questions, 1,999 related questions, and 19,990 comments; this dataset is more reliable than part2. Yet, there is sometimes a bias as, due to the annotation setup, annotators tended to ignore the RelQ when annotating the value for RELC_RELEVANCE2ORGQ.
    Here are the annotation instructions used for part1: http://alt.qcri.org/semeval2016/task3/data/uploads/annotation_instructions_for_part1.pdf

  * train/SemEval2016-Task3-CQA-QL-train-part2.xml
    second part of the TRAIN dataset consisting of 67 more original questions, 670 related questions, and 6,700 comments; this dataset is noisier than part1, as due to the annotation setup, annotators often got confused and filled in the value of RELC_RELEVANCE2ORGQ while wrongly thinking they were actually filling the value for RELC_RELEVANCE2RELQ.
    Here are the annotation instructions used for part2: http://alt.qcri.org/semeval2016/task3/data/uploads/annotation_instructions_for_part2.pdf

  * dev/SemEval2016-Task3-CQA-QL-dev.xml
    DEV dataset consisting of 50 original questions, 500 related questions, and 5,000 comments; this dataset was annotated using the instructions for TRAIN part2, but then the annotations were manually double-checked and are very reliable.


* ALTERNATIVE FORMAT files

  * train/SemEval2016-Task3-CQA-QL-train-part1-with-multiline.xml
    Same as train/SemEval2016-Task3-CQA-QL-train-part1.xml, but also including an uncleansed multi-line version of the questions and the comments.

  * train/SemEval2016-Task3-CQA-QL-train-part2-with-multiline.xml
    Same as train/SemEval2016-Task3-CQA-QL-train-part2.xml, but also including an uncleansed multi-line version of the questions and the comments.

  * dev/SemEval2016-Task3-CQA-QL-dev-with-multiline.xml
    Same as dev/SemEval2016-Task3-CQA-QL-dev.xml, but also including an uncleansed multi-line version of the questions and the comments.


  * train/SemEval2016-Task3-CQA-QL-train-part1-subtaskA.xml
    Same as train/SemEval2016-Task3-CQA-QL-train-part1.xml, but containing only the relevant information for subtask A, with duplicated related questions removed. 

  * train/SemEval2016-Task3-CQA-QL-train-part2-subtaskA.xml
    Same as train/SemEval2016-Task3-CQA-QL-train-part2.xml, but containing only the relevant information for subtask A, with duplicated related questions removed.

  * dev/SemEval2016-Task3-CQA-QL-dev-subtaskA.xml
    Same as dev/SemEval2016-Task3-CQA-QL-dev.xml, but containing only the relevant information for subtask A, with duplicated related questions removed.


  * train/SemEval2016-Task3-CQA-QL-train-part1-subtaskA-with-multiline.xml
    Same as train/SemEval2016-Task3-CQA-QL-train-part1-subtaskA.xml, but also including an uncleansed multi-line version of the questions and the comments.

  * train/SemEval2016-Task3-CQA-QL-train-part2-subtaskA-with-multiline.xml
    Same as train/SemEval2016-Task3-CQA-QL-train-part2-subtaskA.xml, but also including an uncleansed multi-line version of the questions and the comments.

  * dev/SemEval2016-Task3-CQA-QL-dev-subtaskA-with-multiline.xml
    Same as dev/SemEval2016-Task3-CQA-QL-dev-subtaskA.xml, but also including an uncleansed multi-line version of the questions and the comments.


* REFORMATTED files from SemEval-2015 Task 3 (extra training data for subtask A)

  * train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-train-reformatted-multiline.xml
    Reformatted version of the training data from SemEval-2015 Task 3. The text of the questions and the comments is uncleansed and multiline, as it was in 2015.

  * train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-dev-reformatted-multiline.xml
    Reformatted version of the development data from SemEval-2015 Task 3. The text of the questions and the comments is uncleansed and multiline, as it was in 2015.

  * train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-test-reformatted-multiline.xml
    Reformatted version of the testing data from SemEval-2015 Task 3. The text of the questions and the comments is uncleansed and multiline, as it was in 2015.


  * train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-train-reformatted-excluding-2016-questions-multiline.xml
    Reformatted version of the training data from SemEval-2015 Task 3 (excludes the 2016 questions). The text of the questions and the comments is uncleansed and multiline, as it was in 2015.

  * train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-dev-reformatted-excluding-2016-questions-multiline.xml
    Reformatted version of the development data from SemEval-2015 Task 3 (excludes the 2016 questions). The text of the questions and the comments is uncleansed and multiline, as it was in 2015.

  * train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-test-reformatted-excluding-2016-questions-multiline.xml
    Reformatted version of the testing data from SemEval-2015 Task 3 (excludes the 2016 questions). The text of the questions and the comments is uncleansed and multiline, as it was in 2015.


  * train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-train-reformatted-excluding-2016-questions-cleansed.xml
    Same as train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-train-reformatted-excluding-2016-questions-multiline.xml, but with cleansed, single-line questions and comments (as for 2016).

  * train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-dev-reformatted-excluding-2016-questions-cleansed.xml
    Same as train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-dev-reformatted-excluding-2016-questions-multiline.xml, but with cleansed, single-line questions and comments (as for 2016).

  * train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-test-reformatted-excluding-2016-questions-cleansed.xml
    Same as train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-test-reformatted-excluding-2016-questions-multiline.xml, but with cleansed, single-line questions and comments (as for 2016).


* UNANNOTATED data for subtask A
  * http://alt.qcri.org/semeval2016/task3/data/uploads/QL-unannotated-data-subtaskA.xml.zip
    Unannotated data for subtask A: single-line, cleansed.


NOTES:
  1. Some of the related questions are repeated as a question can be potentially related to more than one original question. These repetitions are to be ignored for subtask A. To facilitate this, we have marked them with the tag SubtaskA_Skip_Because_Same_As_RelQuestion_ID="XXX".
  We further provide version of the data with these repetitions removed: *-subtaskA.xml

  2. The reformatted data from SemEval-2015 Task 3 (usable as extra training for subtaks A) has been changed as follows:
    - user IDs were made consistent with this year's user IDs
    - added user names
    - added date of posting for the comments
    - remapped the 2015 annotation labels to the 2016 ones (there were more labels in 2015)
    - fixed the chronological ordering of some comments
    (note that a very small number of comments could not be augmented with the extra metadata, and were thus dropped)
    - NOTE: We also provide a version of the 2015 data where we have excluded from those questions that are already included as related questions in the 2016 data.

  3. This distribution is directly downloadable from the official SemEval-2016 Task 3 website:
  http://alt.qcri.org/semeval2016/task3/index.php?id=data-and-tools



[3] LICENSING

  These datasets are free for general research use.


[4] CITATION

You should use the following citation in your publications whenever using this resource:

@InProceedings{nakov-EtAl:2016:SemEval,
  author    = {Nakov, Preslav  and  M\`{a}rquez, Llu\'{i}s  and  Magdy, Walid  and  Moschitti, Alessandro  and  Glass, Jim  and  Randeree, Bilal},
  title     = {{SemEval}-2016 Task 3: Community Question Answering},
  booktitle = {Proceedings of the 10th International Workshop on Semantic Evaluation},
  series    = {SemEval '16},
  month     = {June},
  year      = {2016},
  address   = {San Diego, California},
  publisher = {Association for Computational Linguistics},
}


[5] SUBTASKS

For ease of explanation, here we list the English subtasks of SemEval-2016 Task 3:

* Subtask A (English): Question-Comment Similarity
  Given a question and the first 10 comments in its question thread, rerank these 10 comments according to their relevance with respect to the question.

* Subtask B (English): Question-Question Similarity
  Given a new question (aka original question) and the set of the first 10 related questions (retrieved by a search engine), rerank the related questions according to their similarity with the original question. 

* Subtask C (English): Question-External Comment Similarity -- this is the main English subtask.
  Given a new question (aka the original question) and the set of the first 10 related questions (retrieved by a search engine), each associated with its first 10 comments appearing in its thread, rerank the 100 comments (10 questions x 10 comments) according to their relevance with respect to the original question.


[6] DATA FORMAT

The datasets are XML-formatted and the text encoding is UTF-8.
Below we focus our description on the format of the main files;
we then briefly describe the format of the alternative format files.

A dataset file is a sequence of examples (original questions):

<root>
  <OrgQuestion> ... </OrgQuestion>
  <OrgQuestion> ... </OrgQuestion>
  ...
  <OrgQuestion> ... </OrgQuestion>
</root>

Each OrgQuestion has an ID, e.g., <OrgQuestion ORGQ_ID="Q1">

The structure of an OrgQuestion is the following:

<OrgQuestion ...>
  <OrgQSubject> text </OrgQSubject>
  <OrgQBody> text </OrgQBody>
  <Thread ...>
    <RelQuestion ...> ... </RelQuestion>
    <RelComment ...> ... </RelComment>
    <RelComment ...> ... </RelComment>
    ...
    <RelComment ...> ... </RelComment>
</OrgQuestion>

The text between the <OrgQSubject> and the </OrgQSubject> tags is the subject of the original question (cleansed version, e.g., with new lines removed and some further minor changes).

The text between the tags <OrgQBody> and </OrgQBody> is the main body of the question (again, this is a cleansed version, e.g., with new lines removed and some further minor changes).

What follows is a Thread, which is a sequence of potentially related questions.
A Thread consists of a potentially relevant question RelQuestion, together with 10 comments RelComment for it.

NOTE: In the *-with-multiline.xml files, <OrgQSubject> and <OrgQBody> contain the original uncleansed text, while the cleansed version of the question (both subject and body, separated by "//") is under <OrgQClean>.


*** Thread ***
A thread has one obligatory and one optional attribute as in the following example:

<Thread THREAD_SEQUENCE="Q1_R4">

<Thread THREAD_SEQUENCE="Q3_R1" SubtaskA_Skip_Because_Same_As_RelQuestion_ID="Q2_R21">

- THREAD_SEQUENCE: (obligatory) internal identifier for the related question. It has the form Qxx_Ryy, where the Qxx is the ID of the original question, and Ryy is the rank of the thread in the list of results returned by a search engine for the original question Qxx.

- SubtaskA_Skip_Because_Same_As_RelQuestion_ID: (optional) present when the current related question thread has already appeared as a related question to some other OrgQuestion; the value of the attribute is the THREAD_SEQUENCE of the first occurrence of this thread in the dataset


*** RelQuestion ***

Each RelQuestion tag has a list of attributes, as in the following example:

<RelQuestion RELQ_ID="Q1_R4" RELQ_RANKING_ORDER="4" RELQ_CATEGORY="Advice and Help" RELQ_DATE="2013-05-02 19:43:00" RELQ_USERID="U1" RELQ_USERNAME="ankukuma" RELQ_RELEVANCE2ORGQ="PerfectMatch">

- RELQ_ID: the same as for the thread (as there is a 1:1 correspondence between a RelQuestion and its thread)
- RELQ_RANKING_ORDER: the rank of the related question thread in the list of results returned by a search engine for the original question
- RELQ_CATEGORY: the question category, according to the Qatar Living taxonomy. Here are some examples of these categories: Advice and Help, Beauty and Style, Cars and driving, Computers and Internet, Doha Shopping, Education, Environment, Family Life in Qatar, Funnies, Health and Fitness, Investment and Finance, Language, Moving to Qatar, Opportunities, Pets and Animals, Politics, Qatar Living Lounge, Qatari Culture, Salary and Allowances, Sightseeing and Tourist attractions, Socialising, Sports in Qatar, Visas and Permits, Welcome to Qatar, Working in Qatar.
- RELQ_DATE: date of posting
- RELQ_USERID: internal identifier for the user who posted the question; consistent across all questions and across all datasets
- RELQ_USERNAME: the name of the user who posted the question; consistent across questions and comments; note that users can change their names over time, and this field shows the latest name the user used (but this name is consistent across the questions, comments and the datasets)
- RELQ_RELEVANCE2ORGQ: relevance of the thread of this RelQuestion with respect to the OrgQuestion. This label could be 
  - PerfectMatch: RelQuestion matches OrgQuestion (almost) perfectly (at test time, this is to be merged with Relevant)
  - Relevant: RelQuestion covers some aspects of OrgQuestion
  - Irrelevant: RelQuestion covers no aspects of OrgQuestion

The structure of a RelQuestion is the following:

<RelQuestion ...>
  <RelQSubject> text </RelQSubject>
  <RelQBody> text </RelQBody>
</RelQuestion>

The text between the <RelQSubject> and the </RelQSubject> tags is the subject of the related question.
The text between tags <RelQBody> and </RelQBody> is the main body of the related question.

NOTE: In the *-with-multiline.xml files, <RelQSubject> and <RelQBody> contain the original uncleansed text, while the cleansed version of the question (both subject and body, separated by "//") is under <RelQClean>.


*** RelComment ***

Each RelComment tag has a list of attributes, as in the following example:

<RelComment RELC_ID="Q104_R22_C1" RELC_DATE="2012-01-09 11:39:52" RELC_USERID="U2011" RELC_USERNAME="drsam" RELC_RELEVANCE2ORGQ="Bad" RELC_RELEVANCE2RELQ="Good">

 - RELC_ID: internal identifier of the comment
 - RELC_USERID: internal identifier of the user posting the comment
 - RELC_USERNAME: the name of the user who posted the comment; consistent across questions and comments; note that users can change their names over time, and this field shows the latest name the user used
 - RELC_RELEVANCE2ORGQ: human assessment about whether the comment is "Good", "Bad", or "PotentiallyUseful" with respect to the *original* question, OrgQuestion
     - Good: at least one subquestion is directly answered by a portion of the comment
     - PotentiallyUseful: no subquestion is directly answered, but the comment gives potentially useful information about one or more subquestions (at test time, this class will be merged with "Bad")
     - Bad: no subquestion is answered and no useful information is provided (e.g., the answer is another question, a thanks, dialog with another user, a joke, irony, attack of other users, or is not in English, etc.).
- RELC_RELEVANCE2RELQ: human assessment about whether the comment is "Good", "Bad", or "PotentiallyUseful" (the latter two will be merged under "Bad" at test time) with respect to the *related* question, RelQuestion
 
Comments are structured as follows:

<RelComment ...>
  <RelCText> text </RelCText>
</RelComment>

The text between the <RelCText> and the </RelCText> tags is the text of the comment.

NOTE: In the *-with-multiline.xml files, <RelCBody> contain the original uncleansed text, while the cleansed version of the comment (both subject and body, separated by "//") is under <RelCClean>.


[7] MORE INFORMATION ABOUT THE CQA-QL CORPUS

The source of the CQA-QL corpus is the Qatar Living Forum (http://www.qatarliving.com). A sample of questions and comments threads was automatically selected, manually filtered and annotated with the categories defined in the task.

After a first internal labeling of a small dataset by several independent annotators, we defined the annotation procedure and we prepared detailed annotation guidelines. 

CrowdFlower was used to collect the human annotations for the large corpus. In all HITs, we collected the annotation of several annotators for each decision (there were at least three human annotators) and we resolved the discrepancies using the mechanisms of CrowdFlower. Unlike SemEval-2015 Task 3, this time we did not eliminate any comments, and thus there is a guarantee that for each question thread, we have the first 10 comments without any comment being skipped.


[8] STATISTICS

Some statistics about the datasets (training & development):

TRAIN-part1: (higher quality)
- ORIGINAL QUESTIONS:
    - TOTAL:                        200
- RELATED QUESTIONS:
    - TOTAL:                      1,999 (<-- subtask B)
        - PerfectMatch:             181 (at test time, merged with "Relevant")
        - Relevant:                 606
        - Irrelevant:             1,212
- RELATED COMMENTS:
    - wrt ORIGINAL QUESTION:
        - TOTAL:                 19,990 (<-- subtask C)
            - Good:               1,988
            - Bad:               16,319
            - PotentiallyUseful:  1,683 (at test time, merged with "Bad")
    - wrt RELATED QUESTION: 
        - TOTAL:                 14,110 (<-- subtask A)
            - Good:               5,287
            - Bad:                6,362
            - PotentiallyUseful:  2,461 (at test time, merged with "Bad")

TRAIN-part2: (lower quality)
- ORIGINAL QUESTIONS:
    - TOTAL:                        67
- RELATED QUESTIONS: (subtask B)
    - TOTAL:                       670 (<-- subtask B)
        - PerfectMatch:             54 (at test time, merged with "Relevant")
        - Relevant:                242
        - Irrelevant:              374
- RELATED COMMENTS:
    - wrt ORIGINAL QUESTION:
        - TOTAL:                 6,700 (<-- subtask C)
            - Good:                849
            - Bad:               5,154
            - PotentiallyUseful:   697 (at test time, merged with "Bad")
    - wrt RELATED QUESTION: 
        - TOTAL:                 3,790 (<-- subtask A)
            - Good:              1,364
            - Bad:               1,777
            - PotentiallyUseful:   649 (at test time, merged with "Bad")


DEV: (highest quality)
- ORIGINAL QUESTIONS:
    - TOTAL:                        50
- RELATED QUESTIONS: (subtask B)
    - TOTAL:                       500 (<-- subtask B)
        - PerfectMatch:             59 (at test time, merged with "Relevant")
        - Relevant:                155
        - Irrelevant:              286
- RELATED COMMENTS:
    - wrt ORIGINAL QUESTION:
        - TOTAL:                 5,000 (<-- subtask C)
            - Good:                345
            - Bad:               4,061
            - PotentiallyUseful:   594 (at test time, merged with "Bad")
    - wrt RELATED QUESTION: 
        - TOTAL:                 2,440 (<-- subtask A)
            - Good:                818
            - Bad:               1,209
            - PotentiallyUseful:   413 (at test time, merged with "Bad")

---------------------------------------------------------------------------

- from 2015: TRAIN-2015-REFORMATTED:
    - QUESTIONS: 2,600
    - COMMENTS:
        - TOTAL:                16,382 (<-- subtask A)
            - Good:              8,035
            - Bad:               6,702
            - PotentiallyUseful: 1,645 (at test time, merged with "Bad")

- from 2015: DEV-2015-REFORMATTED:
    - QUESTIONS: 300
    - COMMENTS:
        - TOTAL:                 1,619 (<-- subtask A)
            - Good:                866
            - Bad:                 569
            - PotentiallyUseful:   184 (at test time, merged with "Bad")

- from 2015: TEST-2015-REFORMATTED:
    - QUESTIONS: 329
    - COMMENTS:
        - TOTAL:                 1,947 (<-- subtask A)
            - Good:                991
            - Bad:                 789
            - PotentiallyUseful:   167 (at test time, merged with "Bad")


---------------------------------------------------------------------------

- from 2015: TRAIN-2015-REFORMATTED:
    - QUESTIONS: 2,480
    - COMMENTS:
        - TOTAL:                14,893 (<-- subtask A)
            - Good:              7,418
            - Bad:               5,971
            - PotentiallyUseful: 1,504 (at test time, merged with "Bad")

- from 2015: DEV-2015-REFORMATTED:
    - QUESTIONS: 291
    - COMMENTS:
        - TOTAL:                 1,529 (<-- subtask A)
            - Good:                813
            - Bad:                 544
            - PotentiallyUseful:   172 (at test time, merged with "Bad")

- from 2015: TEST-2015-REFORMATTED:
    - QUESTIONS: 319
    - COMMENTS:
        - TOTAL:                 1,876 (<-- subtask A)
            - Good:                946
            - Bad:                 774
            - PotentiallyUseful:   156 (at test time, merged with "Bad")

---------------------------------------------------------------------------

<<< ALL DATA PER SUBTASK >>>

- SUBTASK A: (all)
  - Questions:  1,999 +   670 +   500 + 2,600  +   300 +   329 =  6,398
  - Comments : 14,110 + 3,790 + 2,440 + 16,382 + 1,619 + 1,947 = 40,288

- SUBTASK A: (excluding from 2015 the questions that appear as related in 2016)
  - Questions:  1,999 +   670 +   500 + 2,480  +   291 +   319 =  6,259
  - Comments : 14,110 + 3,790 + 2,440 + 14,893 + 1,529 + 1,876 = 38,638

- SUBTASK B:
  - Original questions:    200 +  67 +  50 =   317
  - Related questions :  1,999 + 670 + 500 = 3,169

- SUBTASK C:
  - Original questions:    200 +    67 +    50 =    317
  - Related questions :  1,999 +   670 +   500 =  3,169
  - Comments          : 19,990 + 6,700 + 5,000 = 31,690


[9] CREDITS

Task Organizers:

  Preslav Nakov, Qatar Computing Research Institute, HBKU
  Lluís Màrquez, Qatar Computing Research Institute, HBKU
  Alessandro Moschitti, Qatar Computing Research Institute, HBKU
  Walid Magdy, Qatar Computing Research Institute, HBKU
  James Glass, CSAIL-MIT
  Bilal Randeree, Qatar Living

Task website: http://alt.qcri.org/semeval2016/task3/

Contact: semeval-cqa@googlegroups.com

Acknowledgments:
  1. We would like to thank Hamdy Mubarak and Abdelhakim Freihat from QCRI who have contributed a lot to the data preparation.
  2. We also thank Salvatore Romeo for reformatting the data from SemEval-2015 Task 3.
  3. This research is developed by the Arabic Language Technologies (ALT) group at Qatar Computing Research Institute (QCRI), HBKU, within the Qatar Foundation in collaboration with MIT. It is part of the Interactive sYstems for Answer Search (Iyas) project.
