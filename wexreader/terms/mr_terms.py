import csv
import nltk
import sys
from collections import defaultdict
from nltk.stem.snowball import EnglishStemmer
from mrjob.job import MRJob

# https://gist.githubusercontent.com/bogdan-ivanov/7203659/raw/inverted_index.py
class DocTerms(MRJob):
    """ Inverted index datastructure """
    stemmer = EnglishStemmer()
    stopwords = set(nltk.corpus.stopwords.words('english'))

    def transform(self, word):
		word = word.lower()
    		if self.stemmer:
			try:
    				word = self.stemmer.stem(word)
			except:
				return word
		return word
    
    def mapper(self, line_no, line):
		data = line.split('\t')
		document = data[4].decode('utf-8').lower().replace('\\n', '\n')
		for token in [t.lower() for t in nltk.word_tokenize(document)]:
			if token in self.stopwords:
				continue
			token = self.transform(token)
			yield data[1], token

    def reducer(self, doc_title, tokens):
		index = {}
		for token in tokens:
			if token in index:
				index[token] += 1
			else:
				index[token] = 1
		yield doc_title, index
		
if __name__ == '__main__':
    DocTerms.run()	
