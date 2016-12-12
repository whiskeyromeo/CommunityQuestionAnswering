===================================================================================
Test output format checkers for SemEval-2016 Task 3: "Community Question Answering"
Version 1.0: February 3, 2016
===================================================================================

SUMMARY

	The test output format checkers check the output format for SemEval-2016 Task 3.
	There is a separate checking script for each subtask.


EXAMPLE USE

perl SemEval2016_task3_English_format_checker_subtaskA.pl examples/SemEval2016-Task3-CQA-QL-test-subtaskA.xml.subtaskA.pred.OK
perl SemEval2016_task3_English_format_checker_subtaskA.pl examples/SemEval2016-Task3-CQA-QL-test-subtaskA.xml.subtaskA.pred.Bad

perl SemEval2016_task3_English_format_checker_subtaskB.pl examples/SemEval2016-Task3-CQA-QL-test.xml.subtaskB.pred.OK
perl SemEval2016_task3_English_format_checker_subtaskB.pl examples/SemEval2016-Task3-CQA-QL-test.xml.subtaskB.pred.Bad

perl SemEval2016_task3_English_format_checker_subtaskC.pl examples/SemEval2016-Task3-CQA-QL-test.xml.subtaskC.pred.OK
perl SemEval2016_task3_English_format_checker_subtaskC.pl examples/SemEval2016-Task3-CQA-QL-test.xml.subtaskC.pred.Bad

perl SemEval2016_task3_Arabic_format_checker_subtaskD.pl examples/SemEval2016-Task3-CQA-MD-test-subtaskD.xml.pred.OK
perl SemEval2016_task3_Arabic_format_checker_subtaskD.pl examples/SemEval2016-Task3-CQA-MD-test-subtaskD.xml.pred.Bad



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
