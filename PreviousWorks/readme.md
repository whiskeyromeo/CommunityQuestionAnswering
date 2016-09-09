## Analysis of Previous Works

###Voltron: A Hybrid System For Answer Validation Based on Lexical and Distance Features
**Implementation of Subtask A**
* A: Classification of answer to question as Good, Bad, or Potentially Useful

**Tools**

* Preprocessing: GATE(Cunningham et. al 2002)
* Classification: MALLET(McCallum and Kachites, 2002)
* Distance metrics based on word2vec(Mikolov et. al 2013a) and DKPro Similarity(Bar, et al)(de Castilho, 2014)
	> "we use a combination of surface, morphological, syntactic, and contextual features as well as distance metrics between the question and answer"

**Methods**
> "Our approach is to measure the relatednes of a comment to the question or measure if a question-comment pair is consistent...we attempt to classify each pair as Good, Potential, or Bad"

* Did not organize the whole text according to the structure of reult matrix, as occurs in Vector Space Models(VSMs)
	* Higher scores obtained from Vector Space Models
* Uses n-grams, cosine similarity

	> "We assume that when answering a question, people tend to use the same words with which the question was asked becasue that would make it easier for the question author to understand. Therefore, similar wording and especially similar phrases would be an indication of more informative comment"

* Tokens not punctuation or stop words are considered meaningful

	>"For every meaningful token we extract its stem, lemma, and orthography"

* N-Grams
	* Use bigrams and trigrams, n>= 4 assumed to adversely impact training time
* Bad Answers
	* Assumed:
	
	> Bad comments often include a lot of punctuation, more than one question in the answer...exclamations

* Structural Features
	* named entities given more weight via GATE's build-in NER tools
* TF Vector Space Features
	* DKPros implementation of cosine similarity to compute similar wording(higher cosine similarity = similar wording)
* Word2Vec Semantic Similarity

	> "For a given question-comment pair, we extract word2vec vectors from a pre-trained set for all tokens for which one is available. We compute the centroids for the question and the comment, then use the cosine between the two as a feature. The intention is to capture the similarity between different terms in the pair...the same proc is applied once more for only noun phrase tokens as they carry more information about the topic"

**Classifier Model**
* MALLET : 

	> calculates term-frequency feature vectors from its input documents. These vectors are fed to a MaxEnt classifier, trained and evaluated using tenfold cross validation. For final classification the trained classsifier outputs class probabilities for each of the tree desired categories.

**Experiment/Results**

* baseline :
	* uses only word stokens, sentence, question and answer length, as well as bigrams and trigrams of the q-a pair
	* Very weak : *gold-standard* = 44.18%, *baseline* = 24.05%
* baseline + GATE gazetteers(named entities, etc...) :
	* improvement of 1% : 25.33%
* baseline + DKPro cosine similarity:
	* improvement of +- 4%
* baseline + word2vec:
 	* no improvement
 	* used set of vectors trained on Google News, not vectors specifically trained for SemEval
* Combination of all features:
	* improvement to 50% accuracy and 32.02% F1
* Final Submissions: Combination
	* Trained on SemEval development data *twice*
	* improvement of 14% in F1 score, to 62.35% in accuracy

***

***

###SemanticZ at SemEval-2016 Task 3
**Implementation of Subtasks A and C**

* A: Ranking

**Tools**

* Word2Vec(Mikolov et. al 2013)
* Preprocessing(in order):
	* replacement:
		* url with TOKEN_URL
		* numbers with TOKEN_NUM
		* images with TOKEN_IMG
		* emoticons with TOKEN_EMO
	* tokenized text by matching only continuous alphabet characters including _(underscore)
	* lowercased the result
	* performed removal of stopwords with nltk
* POS Tagging: Stanford tagger(Toutanova et al. 2003)
* L2-regularized logistic regression classifier as in Liblinear( Fan et al. 2008)

**Method**
>"We approach subtask A as a classification problem. For each comment, we extract a variety of features from both the question and the comment, and we train a classifier to label comments as Good or Bad with respect to the therad question. We rank according to the classifier's score of being classified as Good with respect to the question".
	
* Word2Vec:
	* Semantic Word Embeddings
		* obtained from word2vec models trained on different unannotated data sources including QatarLiving and DohaNews
		* For each piece of text, constructed centroid vector from the vectors of all words in that text(after preprocessing, e.g. no stopwords)
	* Semantic Vector Similarities:
		* Question 2 Answer:
			* assumed a relevant answer should have a centroid vector that is close to that for the question.
		* Maximized Similarity:
			* ranked each word in the answer to the question body centroid vector according to similarity and took average similarity of the top N words. 
			* Took the top 1,2,3, and 5 words similarities as features. 
			* assumption that if average similarity for the top N most similar words is high, answer might be relevant
		* Aligned Similarity:
			* For each word, chose the most similar from text and took the average of all best word pair similarities
	* Word Clusters(WC) Similarity:
		* clustered the Word2Vec vocab in 1,000 clusters using K-Means
		* calculated cluster similarity between question word and answer word clusters
		* For all experiments, model trained on QatarLiving forums
			* vector size = 100
			* window size = 10
			* min. word freq = 5
			* skip-gram = 1
	* Latent Dirichlet Allocation(LDA) topic Similarity:
		* built models with 100 topics
		* for each word in question and comment text, build a bag-of-topics with corresponding distribution, calculating the similarity
		* assumption if question and comment share topics, they're more likely to be relevant
	* MetaData: 
		* Answer contains a question mark - bad answer?
		* Answer Length - more clarity with longer?
		* Question Length - more clarity with longer?
		* Question to comment length - question long/answer short less relevant?
		* Answer author is same as corresponding question's author - if answer posted by author, why did they ask the question?
		* Answer rank in thread
		* Question category

**Classifier**

* Concatenated features in a bag of features vector
	* scaled in the 0 to 1 range
* Used different feature configurations
* tuned classifier with varying values of cost parameter, taking one with best accuracy
* used binary classification(good v bad), output a label of either good or bad
	* 0 <= P(good) <= 1
* probability(P(good)) used as relevance rank for each comment

**Experiments** 

* Qatar Living Forum(QLF) Data performed best, second QLF+GoogleNews+DohaNews
* Best results initially from word vectors of size 800
	* resulted in significant slowdown
* Exceeded MAP of above by using better parameters	
	* vector size = 200, window size = 5, min. word freq = 1, skip-gram = 3
* Best Accuracy:
	* vector size = 200, window size = 5, min. word freq = 1, skip-gram = 1
	* vector size = 100, window size = 10, min. word freq = 5, skip-gram = 1

**Results**
* Second Place for Subtask A

**Ideas**

* MTE-NN system with best performing word embeddings models and features
* troll user features(Mihaylov et al.2015a/b) and PMI-based goodness polarity lexicons as in PMI-Cool
* Rich knowledge Sources(SUper Team system)
* Use information from entire threads to make better predictions
	
	> using thread level information for answer classification has already been shown useful...by using features modeling the thread structure and dialogue or by applying threadlevel inference using the predictions of local classifiers

***

***

###SUper Team at SemEval-2016 Task 3
**Implementation of Subtasks A,B, and C**

* A: Q-A Ranking
* B: Q-Q Ranking


**Tools**

* Preprocessing/Feature Extraction: based on Zamanov(Voltron)
* 




