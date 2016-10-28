import nltk

class Preprocessor:


    @staticmethod
    def preprocessQuestion(questions):
        print("\nPreprocessor: words")
        questions = Preprocessor.preprocessAddWords(questions)
        print("\nPreprocessor: stopwords")
        questions = Preprocessor.preprocessStopwords(questions)
        print("\nPreprocessor: parts of speech")
        questions = Preprocessor.preprocessPartOfSpeech(questions)
        print("\nPreprocessor: bigrams")
        questions = Preprocessor.preprocessBigram(questions)
        return questions


    # This should augment the QA tree with bigram distributions for each question
    @staticmethod
    def preprocessBigram(QATree):
        for row in QATree:
            row['question_bigram_list'] = list(nltk.bigrams(row['question_words']))
            row['question_bigram_list_nostopwords'] = list(nltk.bigrams(row['question_words_nostopwords']))

        return QATree


    # This should augment the QA tree with bigram distributions for each question
    @staticmethod
    def preprocessPartOfSpeech(QATree):

        for row in QATree:
            row['question_words_pos'] = nltk.pos_tag(row['question_words'])
            row['question_words_pos_nostopwords'] = nltk.pos_tag(row['question_words_nostopwords'])

        return QATree

    @staticmethod
    def preprocessStopwordsList():
        stopwords = nltk.corpus.stopwords.words('english')
        return stopwords


    # This should remove stopwords from the questions and answers
    @staticmethod
    def preprocessStopwords(QATree):

        stopwords = Preprocessor.preprocessStopwordsList()

        for row in QATree:
            # remove stopwords from question_words
            row['question_words_nostopwords'] = [i for i in row['question_words'] if i not in stopwords]

        return QATree


    # This should augment the QA tree with questions and answers split into sentences
    @staticmethod
    def preprocessAddWords(QATree):

        for row in QATree:
            # tokenize the questions into sentences
            # row['question_sentences'] = nltk.sent_tokenize(row['question'])

            # tokenize the questions into words
            row['question_words'] = nltk.word_tokenize(row['question'])

        return QATree