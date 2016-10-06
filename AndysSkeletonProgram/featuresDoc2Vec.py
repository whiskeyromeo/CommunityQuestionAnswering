from gensim import utils
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec, Word2Vec
from nltk.corpus import brown
import pprint


def trainedword2vec(output):
    global data
    try:
        data
    except NameError:
        print("Doc2Vec: Training on Brown Corpus")
        data = Word2Vec(brown.sents())

    return data


def featuresdoc2vec(QAData, output):

    #trained = trainedword2vec(output)

    output.addstring("Test", "This is a test")

    counter = 0
    model = Doc2Vec(alpha=0.025, min_alpha=0.025)
    questions = []

    # flatten all of the sentences into a big array for training Doc2Vec

    print("Doc2Vec: Sentence List")
    for row in QAData:
        tagged = TaggedDocument(words=row['question_words'], tags=['SENT_%s' % counter])
        questions.append(tagged)
        counter += 1

    # Do the training

    print("Doc2Vec: Building Vocab")
    model.build_vocab(questions)

    # Iterate back over each of the sentences and compute vectors for them

    for row in QAData:
        row['question_features_doc2vec'] = model.infer_vector(row['question'])

    return QAData