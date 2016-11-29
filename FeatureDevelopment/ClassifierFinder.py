# ClassifierFinder
#
# This decides which classifier generators we're going to run.
# Default is everything in the "Classifiers" directory, but
# this can be override by the command-line --classifiers argument.

import os, glob
from utilities import argvalueexists, getargvalue


class ClassifierFinder:

    # return the list of classifier modules that should be run.  This is all python files in the Classifiers directory,
    # except __init__.py

    @staticmethod
    def getSelectedClassifierModules():
        classifierDirectory = os.path.dirname(os.path.abspath(__file__)) + "/Classifiers"
        directoryEntries = glob.glob(classifierDirectory + "/[A-Z]*.py")
        allClassifiers = list(map(ClassifierFinder.pathToClassifierName, directoryEntries))
        classifiers = ClassifierFinder.filterByCommandlineArgument(allClassifiers)
        return classifiers

    # takes in a list of classifiers, and then parses the command line (if present) to see if the user has specified
    # a list of classifiers.  If so, filter the classifier list to just the ones the user wants.  Otherwise, return the
    # original list of all classifiers.

    @staticmethod
    def filterByCommandlineArgument(allClassifiers):
        if argvalueexists('classifiers'):
            requestedClassifiers = getargvalue('classifiers', False).lower().split(',')
            classifiers = []
            for classifier in allClassifiers:
                if classifier.lower() in requestedClassifiers:
                    classifiers.append(classifier)
        else:
            classifiers = allClassifiers
        return classifiers

    # take in a full path to a classifier (python script), and return just the filename, without the path or .py

    @staticmethod
    def pathToClassifierName(classifier):
        parts = classifier.split(os.sep)
        return parts.pop()[:-3]