# The goal is to separate the data into questions and answers
# This is the general idea, we need to sort these into groups
# I'm uploading this knowing that it isn't good code, just so
# people can see how to parse XML at some basic level
# reviewed code from the element tree api
# todo <figure out how to set the default commented header>

# imported plenty of things I didn't need while trying all of them out
# I'll leave them in case anyone wants to explore them
# parsing to tokens, part of speech tagging, chunking, etc are easy
# the hard part is getting the data into the groups we want to analyze together
# in order to use their characteristics to classify new data
"""freakOfKnuth.py - executes the elementParser function calling on some testData"""
__author__ = "freakOfKnuth"

import nltk, re, pprint
from nltk import word_tokenize
#from NlpFunctions import XmlToString
import xml.etree.ElementTree as ET
#from bs4 import BeautifulSoup

#here you'd put the filepath to whatever data you are parsing
filePath = '../CommunityQuestionAnswering/Data/train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-train-reformatted-excluding-2016-questions-cleansed.xml'

def elementParser(filePath):

    # was a function of mine, realized I didn't need it anymore
    #file = XmlToString(filePath)

    # builds a tree, sets the root
    tree = ET.parse(filePath)
    root = tree.getroot()

    # introductory forloop dealing with root and children
    # for child in root:
    #     print(child.tag, child.attrib)

    # testing different ways to parse out questions and subjects
    # we'll need to parse out, group things, then do NLP(pos,N-gram,etc), then machine learning
    # seems like some sort of merge_sort, etc would get us grouped by subject, question, etc
    # then we could analyze things in different grouping and try to project that onto new data with machine learning
    for Thread in root.findall('Thread'):
        relQuestion = Thread.find('RelQuestion')
        subject = relQuestion.find('RelQSubject').text
        print((relQuestion.get('RELQ_CATEGORY')), subject)


# calls the function
elementParser(filePath)