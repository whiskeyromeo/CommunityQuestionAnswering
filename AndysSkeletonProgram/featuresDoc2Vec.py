from gensim import utils
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec, Word2Vec
from nltk.corpus import brown
import pprint


def trainedword2vec():
    global data
    try:
        data
    except NameError:
        data = Word2Vec(brown.sents())

    return data


def featuresdoc2vec(QAData):

    trained = trainedword2vec()
    counter = 0
    model = Doc2Vec(alpha=0.025, min_alpha=0.025)
    sentences = []

    # flatten all of the sentences into a big array for training Doc2Vec

    print("Doc2Vec: Sentence List")
    for row in QAData:
        for sentence in row['question_sentences']:
            sentences.append(TaggedDocument(words=sentence.split(), tags=['SENT_%s' % counter]))
            counter += 1

    pprint.pprint(sentences)

    # Do the training

    print("Doc2Vec: Building sentences")
    model.build_vocab(sentences)

    # Iterate back over each of the sentences and compute vectors for them

    for row in QAData:
        row['question_sentence_vectors'] = []
        for sentence in row['question_sentences']:
            row['question_sentence_vectors'].append(model.infer_vector(sentence))

    return QAData