''' Takes the input of a question vector and a list of lists which contains high dimensional vectors and
    computes & returns the cosine similarity of all the vectors in the list with the new question vector'''
import math

def cosineSimilarity(questionNew = [], questionCollection = [[]]):

    '''dot product of two lists'''
    def dotProduct(x = [], y = []):
        total = 0
        for component,element in zip(x,y):
            prod = component * element
            total = total + prod
        return total

    '''sum of the squares of vector components'''
    def sumSquares(x = []):
        total = 0
        for component in x:
            sqr = component * component
            total = total + sqr
        return total

    '''main method'''
    cosineSimilarity = 0
    cosineSimilarityMatrix = []
    for list in range(len(questionCollection)):
        numerator = dotProduct(questionNew,questionCollection[list])
        denominator = math.sqrt(sumSquares(questionNew)) * math.sqrt(sumSquares(questionCollection[list]))
        cosineSimilarity = numerator/denominator
        cosineSimilarityMatrix.append(cosineSimilarity)

    return cosineSimilarityMatrix

# testQ = [1,2,3]
# testC = [[1,2,3],[-1,-2,-3],[-1,-2,3]]
# cosineMatrix = cosineSimilarity(testQ, testC)
# print(cosineMatrix)

