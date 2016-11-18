
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


class Perfectness:

    def classify(self, trainingQuestions, testingQuestions, FeatureNames):
        models = self.train(trainingQuestions, FeatureNames)
        output = self.predict(testingQuestions, FeatureNames, models)
        output = output.mean(axis=1)
        return output

    def predict(self, questions, FeatureNames, models):
        output = {}
        index = self.getIndex(questions)
        featureMatrix = self.getFeatureMatrix(questions, FeatureNames, index)
        output = pandas.DataFrame()
        for name, model in models:
            print("Predicting with %s model" % name)
            if name == 'SVM':
                modelOutput = model.predict(featureMatrix)
            else:
                modelOutput = numpy.array(model.predict_proba(featureMatrix))[:,1]
            output[name] = pandas.Series(modelOutput, index=index)
        return output

    def train(self, questions, FeatureNames):
        index = self.getIndex(questions)
        featureMatrix = self.getFeatureMatrix(questions, FeatureNames, index)
        labelVector = self.getLabelVector(questions, index)

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

    def getFeatureMatrix(self, questions, names, index):
        features = []
        for q in questions:
            for r in questions[q]['related']:
                features.append(questions[q]['related'][r]['featureVector'])
        featuresDataFrame = pandas.DataFrame(features, index=index, columns=names)
        return featuresDataFrame

    def getLabelVector(self, questions, index):
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

    def getIndex(self, questions):
        index = []
        for q in questions:
            for r in questions[q]['related']:
                index.append(questions[q]['related'][r]['id'])
        return index
