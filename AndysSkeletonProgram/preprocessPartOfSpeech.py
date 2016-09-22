import nltk


# This should augment the QA tree with bigram distributions for each question
def preprocessPartOfSpeech(QATree):

    for row in QATree:
        row['question_words_pos'] = nltk.pos_tag(row['question_words'])

    return QATree