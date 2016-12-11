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
            '../../Data/train/SemEval2016-Task3-CQA-QL-train-part1.xml',
            '../../Data/train/SemEval2016-Task3-CQA-QL-train-part2.xml',
            '../../Data/english_scorer_and_random_baselines_v2.2/SemEval2016-Task3-CQA-QL-dev.xml',
        ]
        return filePaths


    @staticmethod
    def loadXMLQuestions(filenames):
        output = {}
        for filePath in filenames:
            print("\nParsing %s" % filePath)
            fileoutput = Loader.parseTask3TrainingData(filePath)
            print("  Got %s primary questions" % len(fileoutput))
            if not len(fileoutput):
                raise Exception("Failed to load any entries from " + filePath)
            isTraining = "train" in filePath
            for q in fileoutput:
                fileoutput[q]['isTraining'] = isTraining
                for r in fileoutput[q]['related']:
                    fileoutput[q]['related'][r]['isTraining'] = isTraining
            output.update(fileoutput)
        print("\nTotal of %s entries" % len(output))
        return output

    # output format:
    #
    # dict(question_id => dict(
    #   question
    #   id
    #   subject
    #   comments = {}
    #   related = dict(related_id => dict(
    #     question
    #     id
    #     subject
    #     relevance
    #     comments = dict(comment_id => dict(
    #       comment
    #       date
    #       id
    #       username
    #     )
    #   )
    # )
    @staticmethod
    def parseTask3TrainingData(filepath):
        tree = ElementTree.parse(filepath)
        root = tree.getroot()
        OrgQuestions = {}
        for OrgQuestion in root.iter('OrgQuestion'):
            OrgQuestionOutput = {}
            OrgQuestionOutput['id'] = OrgQuestion.attrib['ORGQ_ID']
            OrgQuestionOutput['subject'] = OrgQuestion.find('OrgQSubject').text
            OrgQuestionOutput['question'] = OrgQuestion.find('OrgQBody').text
            OrgQuestionOutput['comments'] = {}
            OrgQuestionOutput['related'] = {}
            OrgQuestionOutput['featureVector'] = []
            if OrgQuestionOutput['id'] not in OrgQuestions:
                OrgQuestions[OrgQuestionOutput['id']] = OrgQuestionOutput
            for RelQuestion in OrgQuestion.iter('RelQuestion'):
                RelQuestionOutput = {}
                RelQuestionOutput['id'] = RelQuestion.attrib['RELQ_ID']
                RelQuestionOutput['subject'] = RelQuestion.find('RelQSubject').text
                RelQuestionOutput['question'] = RelQuestion.find('RelQBody').text
                RelQuestionOutput['givenRelevance'] = RelQuestion.attrib['RELQ_RELEVANCE2ORGQ']
                RelQuestionOutput['givenRank'] = RelQuestion.attrib['RELQ_RANKING_ORDER']
                RelQuestionOutput['comments'] = {}
                RelQuestionOutput['featureVector'] = []
                for RelComment in OrgQuestion.iter('RelComment'):
                    RelCommentOutput = {}
                    RelCommentOutput['id'] = RelComment.attrib['RELC_ID']
                    RelCommentOutput['date'] = RelComment.attrib['RELC_DATE']
                    RelCommentOutput['username'] = RelComment.attrib['RELC_USERNAME']
                    RelCommentOutput['comment'] = RelComment.find('RelCText').text
                    RelQuestionOutput['comments'][RelCommentOutput['id']] = RelCommentOutput
                #if RelQuestionOutput['question'] != None:
                if RelQuestionOutput['question'] == None:
                    RelQuestionOutput['question'] = ""
                OrgQuestions[OrgQuestionOutput['id']]['related'][RelQuestionOutput['id']] = RelQuestionOutput
                #else:
                    #print("Warning: skipping empty question " + RelQuestionOutput['id'])
        return OrgQuestions
