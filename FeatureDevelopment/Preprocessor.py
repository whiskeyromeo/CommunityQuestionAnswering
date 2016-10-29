import nltk
from utilities import forEachQuestion


class Preprocessor:


    @staticmethod
    def preprocessQuestions(questions):
        print("\nPreprocessor: words")
        forEachQuestion(questions, Preprocessor.addWords)
        print("\nPreprocessor: stopwords")
        forEachQuestion(questions, Preprocessor.removeStopwords)
        print("\nPreprocessor: parts of speech")
        forEachQuestion(questions, Preprocessor.addPartOfSpeech)
        print("\nPreprocessor: bigrams")
        forEachQuestion(questions, Preprocessor.addBigrams)



    # This should augment the QA tree with bigram distributions for each question
    @staticmethod
    def addBigrams(question):
        question['question_bigram_list'] = list(nltk.bigrams(question['question_words']))
        question['question_bigram_list_nostopwords'] = list(nltk.bigrams(question['question_words_nostopwords']))


    @staticmethod
    def addPartOfSpeech(question):
        question['question_words_pos'] = nltk.pos_tag(question['question_words'])
        question['question_words_pos_nostopwords'] = nltk.pos_tag(question['question_words_nostopwords'])


    @staticmethod
    def stopwordsList():
        stopwords = nltk.corpus.stopwords.words('english')
        return stopwords


    @staticmethod
    def removeStopwords(question):
        stopwords = Preprocessor.stopwordsList()
        question['question_words_nostopwords'] = [i for i in question['question_words'] if i not in stopwords]


    @staticmethod
    def addWords(question):
        question['question_words'] = nltk.word_tokenize(question['question'])
