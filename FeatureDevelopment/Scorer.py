
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from pprint import pprint
from numpy import ravel
import pandas
import itertools
import numpy


class Scorer:

    @staticmethod
    def rank(questions):
        for q in questions:
            scores = []
            for r in questions[q]['related']:
                scores.append(questions[q]['related'][r]['similarity'])
            scores = sorted(scores)
            for r in questions[q]['related']:
                questions[q]['related'][r]['rank'] = scores.index(questions[q]['related'][r]['similarity'])
            # also redo the given ranks, since they skip steps
            scores = []
            for r in questions[q]['related']:
                scores.append(questions[q]['related'][r]['givenRank'])
            scores = sorted(scores)
            for r in questions[q]['related']:
                questions[q]['related'][r]['givenRank'] = scores.index(questions[q]['related'][r]['givenRank'])

    @staticmethod
    def perfectness(questions, FeatureNames):
        questionCount = len(questions)
        trainCount = round(questionCount * 0.75)
        i = iter(questions.items())
        trainingQuestions = dict(itertools.islice(i, trainCount))
        testingQuestions = dict(i)
        models = Scorer.train(trainingQuestions, FeatureNames)
        output = Scorer.predict(testingQuestions, FeatureNames, models)
        return output

    @staticmethod
    def predict(questions, FeatureNames, models):
        output = {}
        index = Scorer.getIndex(questions)
        featureMatrix = Scorer.getFeatureMatrix(questions, FeatureNames, index)
        output = pandas.DataFrame()
        for name, model in models:
            print("Predicting with %s model" % name)
            if name == 'SVM':
                modelOutput = model.predict(featureMatrix)
            else:
                modelOutput = numpy.array(model.predict_proba(featureMatrix))[:,1]
            output[name] = pandas.Series(modelOutput, index=index)
        return output

    @staticmethod
    def train(questions, FeatureNames):
        index = Scorer.getIndex(questions)
        featureMatrix = Scorer.getFeatureMatrix(questions, FeatureNames, index)
        labelVector = Scorer.getLabelVector(questions, index)

        models = []
        models.append(('LR', LogisticRegression()))
        models.append(('LDA', LinearDiscriminantAnalysis()))
        models.append(('KNN', KNeighborsClassifier()))
        models.append(('CART', DecisionTreeClassifier()))
        models.append(('NB', GaussianNB()))
        models.append(('SVM', SVC()))

        for name, model in models:
            print("Training %s model" % name)
            model.fit(featureMatrix, ravel(labelVector))

        return models

    @staticmethod
    def getFeatureMatrix(questions, names, index):
        features = []
        for q in questions:
            for r in questions[q]['related']:
                features.append(questions[q]['related'][r]['featureVector'])
        featuresDataFrame = pandas.DataFrame(features, index=index, columns=names)
        return featuresDataFrame

    @staticmethod
    def getLabelVector(questions, index):
        labels = []
        for q in questions:
            for r in questions[q]['related']:
                if questions[q]['related'][r]['givenRelevance'] == "PerfectMatch":
                    label = 1
                else:
                    label = 0
                labels.append(label)
        labelDataFrame = pandas.DataFrame(labels, index=index, columns=['Label'])
        return labelDataFrame

    @staticmethod
    def getIndex(questions):
        index = []
        for q in questions:
            for r in questions[q]['related']:
                index.append(questions[q]['related'][r]['id'])
        return index
