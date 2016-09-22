import nltk


# This should augment the QA tree with questions and answers split into sentences
def preprocessAddSentencesAndWords(QATree):

    for row in QATree:
        # tokenize the questions into sentences
        row['question_sentences'] = nltk.sent_tokenize(row['question'])

        # tokenize the questions into words
        row['question_words'] = nltk.word_tokenize(row['question'])

    return QATree