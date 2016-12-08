from Loader import Loader
from Preprocessor import Preprocessor


loader = Loader()
prep = Preprocessor()

questions = loader.loadXMLQuestions(loader.getfilenames())

prep.preprocessQuestions(questions)

