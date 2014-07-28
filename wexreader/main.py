# sudo apt-get install python-numpy python-scipy
# sudo apt-get install python-dev
# sudo apt-get install libatlas-base-dev gfortran

import os
import sys
import csv
import re
import os
import math
from xml.etree import ElementTree
import nltk
from nltk.corpus import XMLCorpusReader
from nltk.corpus import WordListCorpusReader

from nltk.tokenize import line_tokenize 
from collections import defaultdict
from nltk.stem.snowball import EnglishStemmer
import sklearn

csv.field_size_limit(sys.maxsize)

from sklearn.feature_extraction.text import TfidfVectorizer


# https://gist.githubusercontent.com/bogdan-ivanov/7203659/raw/inverted_index.py
class Index:
    """ Inverted index datastructure """
    def __init__(self, tokenizer, stemmer=None, stopwords=None):
		"""
		tokenizer   -- NLTK compatible tokenizer function
		stemmer     -- NLTK compatible stemmer 
		stopwords   -- list of ignored words
		"""
		self.tokenizer = tokenizer
		self.stemmer = stemmer
		self.index = defaultdict(lambda: defaultdict(lambda: 0))
		self.documents = {}
		self.__unique_id = 0
		if not stopwords:
			self.stopwords = set()
		else:
			self.stopwords = set(stopwords)

    def transform(self, word):
		word = word.lower()
    		if self.stemmer:
    			word = self.stemmer.stem(word)
		return word
	
    def lookup(self, word):
		"""
		Lookup a word in the index
		"""
		word = self.transform(word) 
		return [self.documents.get(id, None) for id in self.index.get(word)]
    
    def add(self, document):
		"""
		Add a document string to the index
		"""
		document = document.replace('\\n', '\n')
		for token in [t.lower() for t in nltk.word_tokenize(document)]:
			if token in self.stopwords:
				continue
			token = self.transform(token)
			self.index[token][self.__unique_id] += 1
		self.documents[self.__unique_id] = document
		self.__unique_id += 1
		return
	
    def tfidf(self, word, document): 
		word = self.transform(word)
		feature_map = self.index[word]
		
		tf = feature_map[document]
		documents = sum([1 for (k,v) in feature_map.items() if v > 0])
		if documents == 0:
			return 0
		idf = math.log( self.__unique_id * 1.0 / documents)
		return tf * idf

stopwords = nltk.corpus.stopwords.words('english')
index = Index(nltk.word_tokenize, 
  EnglishStemmer(), 
  nltk.corpus.stopwords.words('english'))

count = 1
tsv = open("../data/subset.tsv")
for line in csv.reader(tsv, dialect="excel-tab"): #You can also use delimiter="\t" rather than giving a dialect.
	data = line[4]
	# tokens = nltk.word_tokenize(data.lower())


	# tfidf = sklearn.feature_extraction.text.TfidfTransformer()
	# tfs = tfidf.fit_transform(tokens);
	# print tfs
	print "Adding document:", line[1], count
	index.add(data.decode('utf-8').lower())
	# for x in index.index:
	#     print (x)

	# filteredtokens =  [w for w in tokens if w not in stopwords]
	# # for token in tokens:
	# #     print token
	# #     if token.lower() not in stopwords:
	# #         filteredtokens.push(token) 
	# print filteredtokens

	# text = nltk.Text(filteredtokens)
	# text.collocations()
	count += 1
	if count > 5:
		break

tfidfs = [index.tfidf('country', x) for x in range(0,5)]
print tfidfs
