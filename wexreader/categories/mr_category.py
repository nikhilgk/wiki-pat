import csv
import nltk
import sys
import re
from collections import defaultdict
from nltk.stem.snowball import EnglishStemmer
from mrjob.job import MRJob

class Category(MRJob):

    def mapper(self, line_no, line):
		data = line.split('\t')
		xml = data[3]
		result = re.finditer('(Category:[^<]*)', xml)
		categories = [m.group(0).replace('Category:','') for m in result]
		for category in categories:
			yield category, data[1]

    def reducer(self, category, doc_titles):
		category_docs = []
		for doc_title in doc_titles:
			category_docs.append(doc_title)
		yield category, category_docs
if __name__ == '__main__':
    Category.run()	
