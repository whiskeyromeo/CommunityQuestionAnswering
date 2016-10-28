# Andy/Emily/Josh's feature development sandbox
#
# This program loads a set of question-to-question data, runs a set experimental feature vector generators,
# and feeds their combined output into an interative analysis module.
#
# This is not meant to be a complete contest entry, but a place to experiment with three sets of code:
# - loading/preprocessing questions
# - feature generation
# - iterative analysis
#
# By default it runs all features in the Features directory.  To only run specific features, pass
# --features=[Feature1,Feature2,etc] on the command line.


from FeatureFinder import FeatureFinder
from Loader import Loader
from Preprocessor import Preprocessor
from Features import *
import pickle, sys

# we can cache the output of the loader+preprocessor to disk, to avoid this performance hit
# every time.  If the user wants to use the cached data, load it here and skip the loader+preprocessor

if "--cached" in sys.argv:
    print("Loading cached question and preprocessor data")
    questions = pickle.load(open("questions.pickle", "rb"))

else:
    # Loader

    questionFiles = Loader.getfilenames()
    questions = Loader.loadXMLQuestions(questionFiles)

    # Preprocessors

    questions = Preprocessor.preprocessQuestion(questions)

    # Store the new data as the current cache

    pickle.dump(questions, open("questions.pickle", "wb"))

# Print out question structure for reference

print("\nSample question structure:")
for key in questions[0]:
    print("  " + key + " = " + str(questions[0][key]))

# Feature Generators

featureGenerators = FeatureFinder.getSelectedFeatureModules()
for feature in featureGenerators:
    print("\nRunning feature generator '" + feature + "'")
    featureClass = globals()[feature].__dict__[feature]()
    featureClass.init(questions)
    for question in questions:
        question['featureVector'] += featureClass.createFeatureVector(question)

# Results

print("\nSample questions and feature vectors:")
for i in range(0, 5):
    print('\nQuestion: ' + questions[i]['question'])
    print('Feature Vector: ' + str(questions[i]['featureVector']))

print("\nFinished")