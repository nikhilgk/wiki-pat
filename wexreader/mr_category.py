import csv
import nltk
import sys
import re
from collections import defaultdict
from nltk.stem.snowball import EnglishStemmer
from mrjob.job import MRJob

class Metadata(MRJob):

    def mapper(self, line_no, line):
		data = line.split('\t')
		xml = data[3]
		result = re.finditer('(Category:[^<]*)', xml)
		categories = [m.group(0).replace('Category:','') for m in result]
		yield data[1], categories

    def reducer(self, doc_title, categories):
		for category in categories:
			yield doc_title, category
	
if __name__ == '__main__':
    Metadata.run()	
