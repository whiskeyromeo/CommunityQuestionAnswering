import nltk


# This should augment the QA tree with bigram distributions for each question
def preprocessBigram(QATree, output):

    for row in QATree:
        row['question_bigram'] = nltk.bigrams(row['question_words'])
        row['question_bigram_list'] = list(row['question_bigram'])

    return QATree