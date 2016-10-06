#!/usr/bin/perl
#
#  Author: Preslav Nakov
#  
#  Description: Checks the output format for SemEval-2016 Task 3, subtask A.
#
#  Last modified: February 3, 2016
#

# Example runs:
#    perl SemEval2016_task3_English_format_checker_subtaskA.pl examples/SemEval2016-Task3-CQA-QL-test-subtaskA.xml.subtaskA.pred.OK
#    perl SemEval2016_task3_English_format_checker_subtaskA.pl examples/SemEval2016-Task3-CQA-QL-test-subtaskA.xml.subtaskA.pred.Bad



use warnings;
use strict;
use utf8;


################
###   MAIN   ###
################

die "Use $0 <INPUT_FILE>" if (0 != $#ARGV);
my $INPUT_FILE = $ARGV[0];
my $RANDOM_BASELINE = 'random-refs/SemEval2016-Task3-CQA-QL-test-subtaskA.xml.subtaskA.random_pred';

### 1. Open the files and 
open INPUT, $INPUT_FILE or die;
open REF, $RANDOM_BASELINE or die;
binmode(INPUT, ":utf8");
binmode(REF, ":utf8");

print "JUST A NOTE: the value in column 3 is ignored (instead, column 4 does matter); thus, you can fill column 3 with any value, e.g., with a constant such as 0.\n\n";

while (<INPUT>) {

	# Q318_R6	Q318_R6_C1	0	0.00178272	false
	die "Wrong file format!" if (!/^(Q[0-9]+_R[0-9]+)\t(Q[0-9]+_R[0-9]+_C[0-9]+)\t[0-9]+\t[0-9\.eE\-]+\t(true|false)/);
	my ($qid, $cid) = ($1, $2);

	die "The question ID should be a prefix of the comment ID: $qid <--> $cid" if ($cid !~ /^$qid\_C[0-9]+$/);

	my $refLine = <REF>;
	die "Wrong file format!" if ($refLine !~ /^(Q[0-9]+_R[0-9]+)\t(Q[0-9]+_R[0-9]+_C[0-9]+)\t[0-9]+\t[0-9\.eE\-]+\t(true|false)/);
	my ($refQid, $refCid) = ($1, $2);

	die "Wrong columns 1,2: expected ($refQid, $refCid), but found ($qid, $cid)" if (($qid ne $refQid) || ($cid ne $refCid));

}

### 3. Close the files
close INPUT or die;
close REF or die;

print "<<< The file looks properly formatted. >>>\n";
