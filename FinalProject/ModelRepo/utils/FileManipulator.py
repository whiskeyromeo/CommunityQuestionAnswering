'''
	__author__ = Will Russell
'''

class FileManipulator:

	'''
		FileReader takes the name of a file which is comprised of documents
		and passes the file line by line into an array
		Returns :  the populated array of documents
	'''
	def FileReader(filename):
		documents = []
		file = open(filename, 'r')
		for line in file:
			documents.append(line)
		return documents

	'''
		FileCreator takes a desired filename and and array of documents and creates
		a textfile based on those documents, while removing whitespace and logging to 
		a logfile
	'''
	def FileCreator(filename, documents):
		file = open(filename + '.txt', 'w')
		logging.info('Ready to write to ' + filename)
		for row in documents:
			re.sub('[\s+]',' ', 'row')
			file.write(row + '\n')
		logging.info('Finished writing to ' + filename)


	def prepModelFolder():
		cwd = os.getcwd()
		cwd = cwd.split('/')
		n = len(cwd)
		if(cwd[n-1].lower() == 'vomitrepo'):
			modelPath = './models/'
		else:
			modelPath = '../models/'
		try:
			os.makedirs(modelPath)
		except OSError as e:
			if e.errno != 17:
				raise
			pass
		return modelPath

	'''
		Params: filename : a string representing the desired 
		directory/filename

		Returns : a string representing the destination file to save various 
		formats to with name consistency
	'''
	def CreateFilePath(filename):
		folder_path = './tmp/' + filename
		if not os.path.exists(folder_path):
			os.makedirs(folder_path)
		new_dest = folder_path + '/' + filename
		return new_dest 


	'''
		Takes a string to be used for the name of a textfile and a list of documents
		Creates a file based on the list of documents with each one of the documents
		being on a single row. 
	'''
	def CleanFileCreator(filename, documents):
		# Get over the damned 'ascii' cannot compile error...
		documents = QuestionCleaner(documents)
		reload(sys)
		file = open(filename + '.txt' , 'w')
		logging.info('Ready to write to cleanfile ' + filename)
		for idx, row in enumerate(documents):
			if idx == len(documents)-1:
				file.write(row)
			else:
				file.write(row + '\n')
		logging.info('Finished writing to cleanfile ' + filename)
		reload(sys)
		sys.setdefaultencoding('ascii')

