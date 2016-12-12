#!/usr/bin/perl
#
#  Author: Preslav Nakov
#  
#  Description: Checks the output format for SemEval-2016 Task 3, subtask D.
#
#  Last modified: February 3, 2016
#

# Example runs:
#    perl SemEval2016_task3_Arabic_format_checker_subtaskD.pl examples/SemEval2016-Task3-CQA-MD-test-subtaskD.xml.pred.OK
#    perl SemEval2016_task3_Arabic_format_checker_subtaskD.pl examples/SemEval2016-Task3-CQA-MD-test-subtaskD.xml.pred.Bad



use warnings;
use strict;
use utf8;


################
###   MAIN   ###
################

die "Use $0 <INPUT_FILE>" if (0 != $#ARGV);
my $INPUT_FILE = $ARGV[0];
my $RANDOM_BASELINE = 'random-refs/SemEval2016-Task3-CQA-MD-test-subtaskD.xml.random_pred';

### 1. Open the files and 
open INPUT, $INPUT_FILE or die;
open REF, $RANDOM_BASELINE or die;
binmode(INPUT, ":utf8");
binmode(REF, ":utf8");

print "JUST A NOTE: the value in column 3 is ignored (instead, column 4 does matter); thus, you can fill column 3 with any value, e.g., with a constant such as 0.\n\n";

while (<INPUT>) {

	# 201399	7480	0	0.43562986	false
	die "Wrong file format!" if (!/^([0-9]+)\t([0-9]+)\t[0-9]+\t[0-9\.eE\-]+\t(true|false)/);
	my ($qid, $rqcid) = ($1, $2);

	my $refLine = <REF>;
	die "Wrong file format!" if ($refLine !~ /^([0-9]+)\t([0-9]+)\t[0-9]+\t[0-9\.eE\-]+\t(true|false)/);
	my ($refQid, $refRqcid) = ($1, $2);

	die "Wrong columns 1,2: expected ($refQid, $refRqcid), but found ($qid, $rqcid)" if (($qid ne $refQid) || ($rqcid ne $refRqcid));

}

### 3. Close the files
close INPUT or die;
close REF or die;

print "<<< The file looks properly formatted. >>>\n";
