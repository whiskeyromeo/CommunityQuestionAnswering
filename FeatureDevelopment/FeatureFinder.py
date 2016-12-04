# FeatureFinder
#
# This decides which feature generators we're going to run.
# Default is everything in the "Features" directory, but
# this can be override by the command-line --features argument.

import os, glob
from utilities import argvalueexists, getargvalue
from pprint import pprint


class FeatureFinder:

    # return the list of feature modules that should be run.  This is all python files in the Features directory,
    # except __init__.py

    @staticmethod
    def getSelectedFeatureModules():
        featureDirectory = os.path.dirname(os.path.abspath(__file__)) + "/Features"
        pprint(featureDirectory)
        directoryEntries = glob.glob(featureDirectory + "/[A-Z]*.py")
        allFeatures = list(map(FeatureFinder.pathToFeatureName, directoryEntries))
        features = FeatureFinder.filterByCommandlineArgument(allFeatures)
        return features

    # takes in a list of features, and then parses the command line (if present) to see if the user has specified
    # a list of features.  If so, filter the feature list to just the ones the user wants.  Otherwise, return the
    # original list of all features.

    @staticmethod
    def filterByCommandlineArgument(allFeatures):
        if argvalueexists('features'):
            requestedFeatures = getargvalue('features', False).lower().split(',')
            features = []
            for feature in allFeatures:
                if feature.lower() in requestedFeatures:
                    features.append(feature)
        else:
            features = allFeatures
        return features

    # take in a full path to a feature generator (python script), and return just the filename, without the path or .py

    @staticmethod
    def pathToFeatureName(feature):
        parts = feature.split(os.sep)
        return parts.pop()[:-3]