
class QuestionLength:

    def init(self, allQuestions):
        return

    def createFeatureVector(self, question):
        return [len(question['question_words_nostopwords'])]
