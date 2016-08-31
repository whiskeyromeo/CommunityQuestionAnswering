TEST dataset for SemEval-2016 Task #3: Community Question Answering

Version 1.0: January 11, 2016


SUMMARY

- SemEval2016_task3_test_input_README.txt -- this file

- SUBMISSION_DESCRIPTION_TEMPLATE.txt -- template for describing the submitted runs

English:

  - English/SemEval2016-Task3-CQA-QL-test-input.xml -- test input for subtasks A, B, and C (English). Note that there are repetitions of related questions, and these are to be skipped if you use this file for subtask A (marked with SubtaskA_Skip_Because_Same_As_RelQuestion_ID="XXX").

  - English/SemEval2016-Task3-CQA-QL-test-with-multiline-input.xml -- another version of the test input for subtasks A, B, and C (English), this time also including a multiline version of the questions and answers. Note that there are repetitions of related questions, and these are to be skipped if you use this file for subtask A (marked with SubtaskA_Skip_Because_Same_As_RelQuestion_ID="XXX").

  - English/SemEval2016-Task3-CQA-QL-test-subtaskA-input.xml -- an alternative input for subtask A, which excludes repetitions that are present in SemEval2016-Task3-CQA-QL-test-input.xml

  - English/SemEval2016-Task3-CQA-QL-test-subtaskA-with-multiline-input.xml -- yet another alternative input for subtask A, which excludes repetitions that are present in SemEval2016-Task3-CQA-QL-test-input.xml and also including a multiline version of the questions and answers

*** NOTE: As for TRAIN and DEV, we provide the input in different alternative formats to make the life of participants easier; participants can choose whatever they prefer. Regardless of the input used, the output format is unique and we will require separate output files for each subtask (up to three runs per subtask). There should be 3,270 predictions for subtask A, 700 predictions for subtask B, and 7,000 predictions for subtask C.

Arabic:

  - Arabic/SemEval2016-Task3-CQA-MD-test-input-Arabic.xml -- test input for subtask D (Arabic)


NOTE ON TRAIN/DEV DATA USE

To use these test datasets, the participants should download (1), and most likely also (2) and (3):

1. the training dataset
2. the dev dataset
3. the official scorer (participants would only be able to use it on the dev data)

They can all be found here: 

http://alt.qcri.org/semeval2016/task3/index.php?id=data-and-tools


INPUT DATA FORMAT

  The TEST input data is in the same format as the DEV input data, except that the gold labels are substituted by "?".


EXPECTED OUTPUT FORMAT

See the README of the scorer.


SCORING

See the README of the scorer.


DATASET USE

The development dataset is intended to be used as a development-time evaluation dataset as the participants develop their systems. However, the participants are free to use the dataset in any way they like, e.g., they can add the development dataset to their training data as well.


SUBMISSION NOTES

1. Participants can choose to download the test data at any moment during the evaluation period (January 10-31, 2016). Regardless of the time of download, results are to be submitted by January 31, 2016, 23:59 hours. The time zone is Midway, Midway Islands, United States: see http://www.timeanddate.com/worldclock/city.html?n=1890).

2. The submission will be done using the SemEval START website:

  https://www.softconf.com/naacl2016/SemEval2016/

3. Participants can make new submissions, which will substitute their earlier submissions on the START server multiple times, but only before the deadline (see above). Thus, we advise that participants submit their runs early, and possibly resubmit later if there is time for that (START was not closed).

4. Participants are free to participate for a single subtask or for any combination of subtasks.

5. We allow up to three runs (submissions) per subtask: one primary and two contrastive. The participants must specify which run is primary (to be used for the official ranking) at the time of submission (see below). Having contrastive runs is optional. 

6. Participants are free to use any additional data, but they have to explain this at submission time. Systems using significant additional resources will be appropriately marked in the final ranking.


SUBMISSION PROCEDURE

1. Each participating team should register on 

  http://goo.gl/forms/cGkRocFFph

Only one registration is necessary per team even when participating in multiple tasks.


2. The submission should be a single ZIP file that contains all runs, where the names of the runs can be (a subset of) these:

README.txt -- short description of the submission

subtask_A_primary.txt
subtask_A_contrastive1.txt
subtask_A_contrastive2.txt

subtask_B_primary.txt
subtask_B_contrastive1.txt
subtask_B_contrastive2.txt

subtask_C_primary.txt
subtask_C_contrastive1.txt
subtask_C_contrastive2.txt

subtask_D_primary.txt
subtask_D_contrastive1.txt
subtask_D_contrastive2.txt

3. The name of the ZIP file should match the team's name.

4. The README file should have the format of the SUBMISSION_DESCRIPTION_TEMPLATE.txt.
It should contain the following information (make sure it is clear what applies to subtask A, B, C, and D):

  1. Team ID

  2. Team affiliation

  3. Contact information

  4. Submission, i.e., ZIP file name

  5. System specs

  - 5.1 Core approach

  - 5.2 Supervised or unsupervised

  - 5.3 Important/interesting/novel features used

  - 5.4 Important/interesting/novel tools used

  - 5.5 Significant data pre/post-processing

  - 5.6 Other data used (outside of the provided)

  - 5.7 Did you participate in SemEval-2015 task 3?

  6 References (if applicable)



LICENSE

Licensing: 
- the scripts and all files released for the task are free for general research use 
- you should use one of the following citation in your publications whenever using these resources:

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


CREDITS

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
  1. We would like to thank Hamdy Mubarak, Abdelhakim Freihat, and Salvatore Romeo from QCRI who have contributed a lot to the data preparation.
  2. We also thank Salvatore Romano for reformatting the data from SemEval-2015 Task 3.
  3. This research is developed by the Arabic Language Technologies (ALT) group at Qatar Computing Research Institute (QCRI), HBKU, within the Qatar Foundation in collaboration with MIT. It is part of the Interactive sYstems for Answer Search (Iyas) project.
