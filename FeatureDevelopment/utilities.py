import sys


def getargvalue(name, required):
    output = False
    for arg in sys.argv:
        if arg[2:len(name)+2] == name:
            output = arg[3+len(name):]
    if required and not output:
        raise Exception("Required argument " + name + " not found in sys.argv")
    return output
from scipy import spatial
import math

def argvalueexists(name):
    output = False
    for arg in sys.argv:
        if arg[2:len(name)+2] == name:
            output = True
    return output


def forEachQuestion(questions, function):
    for question in questions:
        function(questions[question])
        for relatedQuestion in questions[question]['related']:
            function(questions[question]['related'][relatedQuestion])


def ellips(text, length):
    if len(text) > length:
        return text[:60] + "..."
    else:
        return text


def cosineSimilarity(questionNew=[], relatedQuestion=[]):

    '''dot product of two lists'''

    def dotProduct(x=[], y=[]):
        total = 0
        for component, element in zip(x, y):
            prod = component * element
            total = total + prod
        return total

    '''sum of the squares of vector components'''

    def sumSquares(x=[]):
        total = 0
        for component in x:
            sqr = component * component
            total = total + sqr
        return total

    '''main method'''
    numerator = dotProduct(questionNew, relatedQuestion)
    denominator = math.sqrt(sumSquares(questionNew)) * math.sqrt(sumSquares(relatedQuestion))
    cosineSimilarity = numerator / denominator

    return cosineSimilarity
