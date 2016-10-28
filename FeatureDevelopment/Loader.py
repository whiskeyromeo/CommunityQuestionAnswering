from utilities import *
import xml.etree.ElementTree as ElementTree


class Loader:
    @staticmethod
    def getfilenames():
        if not argvalueexists("questionfiles"):
            output = Loader.defaultfilenames()
        else:
            output = getargvalue("questionfiles", True).split(",")
        return output


    @staticmethod
    def defaultfilenames():
        filePaths = [
            '../Data/train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-train-reformatted-excluding-2016-questions-cleansed.xml',
            '../Data/train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-dev-reformatted-excluding-2016-questions-cleansed.xml',
            '../Data/train-more-for-subtaskA-from-2015/SemEval2015-Task3-CQA-QL-test-reformatted-excluding-2016-questions-cleansed.xml',
            # '../Data/dev/SemEval2016-Task3-CQA-QL-dev-subtaskA.xml',
            '../Data/train/SemEval2016-Task3-CQA-QL-train-part2-subtaskA.xml',
            '../Data/train/SemEval2016-Task3-CQA-QL-train-part1-subtaskA.xml'
        ]
        return filePaths


    @staticmethod
    def loadXMLQuestions(filenames):
        output = []
        for filePath in filenames:
            print("\nParsing %s" % filePath)
            fileoutput = Loader.elementParser(filePath)
            print("  Got %s entries" % len(fileoutput))
            if not len(fileoutput):
                raise Exception("Failed to load any entries from " + filePath)
            output += fileoutput
        print("\nTotal of %s entries" % len(output))
        return output

    """
    Returns an array populated with questions
    The comments are nested in each question

    Each question will have the following structure:
     - "question" (string)
     - "subject" (string)
     - "threadId" (string)
     - "comments" (list of:)
     -   "comment" (string)
     -   "comment_id" (string)
    """
    @staticmethod
    def elementParser(filepath):
        # construc the Element Tree and get the root
        tree = ElementTree.parse(filepath)
        root = tree.getroot()
        # create a list to store the pulled threads
        threadList = []
        # find each thread in the tree, starting at the root
        for Thread in root.findall('Thread'):
            # create a dict for each question
            QuestionDict = {}
            # find each question
            relQuestion = Thread.find('RelQuestion')
            #Pull the values from the questions into the relevant fields of the question dict
            QuestionDict['threadId'] = relQuestion.attrib['RELQ_ID']
            QuestionDict['subject'] = relQuestion.find('RelQSubject').text
            QuestionDict['question'] = relQuestion.find('RelQBody').text
            QuestionDict['category'] = relQuestion.attrib['RELQ_CATEGORY']
            QuestionDict['username'] = relQuestion.attrib['RELQ_USERNAME']
            comments = []
            # Pull the comments from the filepath
            for relComment in Thread.findall('RelComment'):
                #create a dict for the comment
                commentDict = {}
                #populate the comment dict
                commentDict['comment'] = relComment.find('RelCText').text
                commentDict['comment_id'] = relComment.attrib['RELC_ID']
                comments.append(commentDict)
            # set the comments key to be equal to the question's comments
            QuestionDict['comments'] = comments
            QuestionDict['featureVector'] = []
            #put the comments into the Question object
            if type(QuestionDict['question']) is str:
                threadList.append(QuestionDict)
            #else:
                #print("  Warning: skipping question %s with no question text" % QuestionDict['threadId'])
        return threadList