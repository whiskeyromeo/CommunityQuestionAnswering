from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def untokenize(words):
    """
    Untokenizing a text undoes the tokenizing operation, restoring
    punctuation and spaces to the places that people expect them to be.
    Ideally, `untokenize(tokenize(text))` should be identical to `text`,
    except for line breaks.
    """
    text = ' '.join(words)
    step1 = text.replace("`` ", '"').replace(" ''", '"').replace('. . .',  '...')
    step2 = step1.replace(" ( ", " (").replace(" ) ", ") ")
    step3 = re.sub(r' ([.,:;?!%]+)([ \'"`])', r"\1\2", step2)
    step4 = re.sub(r' ([.,:;?!%]+)$', r"\1", step3)
    step5 = step4.replace(" '", "'").replace(" n't", "n't").replace(
        "can not", "cannot")
    step6 = step5.replace(" ` ", " '")

    return step6.strip()

def editToken( str, type ):
    # This adds the entity to the text and KEEPS the original word
    string = (str + " " + type + "_NER")
    answer = string.decode('utf-8')

    # This REMOVES the original word and just returns the entity
    # answer = (type + "_NER")

    return answer


st = StanfordNERTagger('/Users/owner/Documents/CommunityQuestionAnswering/stanford-ner-2014-06-16/classifiers/english.muc.7class.distsim.crf.ser.gz',
                       '/Users/owner/Documents/CommunityQuestionAnswering/stanford-ner-2014-06-16/stanford-ner.jar',
                       encoding='utf-8')

# This reads the file with all the questions and data in it
# TODO: Get correct name of file
with open('questions.txt', 'r') as sourceFile:
    text=sourceFile.read().replace('\n', '')

tokenized_text = word_tokenize(text)
classified_text = st.tag(tokenized_text)


for index, classified in enumerate(classified_text):
    # for classified, token in zip(classified_text, tokenized_text):
    entity = classified[1]
    if entity != "O":
        tokenized_text[index] = editToken(classified[0], entity)


for index, word in enumerate(tokenized_text):
    tokenized_text[index] = word.decode('utf-8')
finalText = untokenize(tokenized_text)

sourceFile = open('questiosn.txt', 'w')
sourceFile.write(finalText)
sourceFile.truncate()
sourceFile.close()
