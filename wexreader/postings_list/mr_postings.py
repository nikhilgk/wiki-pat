import csv
import nltk
import sys
from sets import Set
from nltk.stem.snowball import EnglishStemmer
from mrjob.job import MRJob

# https://gist.githubusercontent.com/bogdan-ivanov/7203659/raw/inverted_index.py
class PostingsList(MRJob):
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
			yield token, data[1]	

    def reducer(self, token, doc_titles):
		postings_list = {}
		for doc_title in doc_titles:
			postings_list[doc_title] = 1
		yield token, postings_list 
		
if __name__ == '__main__':
    PostingsList.run()	
