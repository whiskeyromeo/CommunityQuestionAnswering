
class AverageWordLength:

    def init(self, allQuestions):
        return

    def createFeatureVector(self, question):
        sum = 0
        count = 0
        for word in question['question_words_nostopwords']:
            sum += len(word)
            count += 1
        return [sum/count]
