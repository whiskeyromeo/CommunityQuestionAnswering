import nltk


def preprocessStopwordsList():
    stopwords = nltk.corpus.stopwords.words('english')
    return stopwords

# This should remvoe stopwords from the questions and answers
def preprocessStopwords(QATree, output):

    stopwords = preprocessStopwordsList()

    for row in QATree:
        # remove stopwords from question_words
        row['question_words'] = [i for i in row['question_words'] if i not in stopwords]

    return QATree