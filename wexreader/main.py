# sudo apt-get install python-numpy python-scipy
# sudo apt-get install python-dev
# sudo apt-get install libatlas-base-dev gfortran

import os
import sys
import csv
import re
import os
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
        self.index = defaultdict(list)
        self.documents = {}
        self.__unique_id = 0
        if not stopwords:
            self.stopwords = set()
        else:
            self.stopwords = set(stopwords)
        
    def lookup(self, word):
        """
        Lookup a word in the index
        """
        word = word.lower()
        if self.stemmer:
            word = self.stemmer.stem(word)
            
        return [self.documents.get(id, None) for id in self.index.get(word)]
    
    def add(self, document):
        """
        Add a document string to the index
        """
        for token in [t.lower() for t in nltk.word_tokenize(document)]:
            if token in self.stopwords:
                continue

            if self.stemmer:
                token = self.stemmer.stem(token)

            if self.__unique_id not in self.index[token]:
                self.index[token].append(self.__unique_id)

        self.documents[self.__unique_id] = document
        self.__unique_id += 1   


stopwords = nltk.corpus.stopwords.words('english')
with open("../data/subset.tsv") as tsv:
    for line in csv.reader(tsv, dialect="excel-tab"): #You can also use delimiter="\t" rather than giving a dialect.
        s = line[3]
        result = re.finditer('(Category:[^<]*)', s)
        for m in result:
            print m.group(0).replace('Category:','')
        data = line[4]
        tokens = nltk.word_tokenize(data.lower())


        tfidf = sklearn.feature_extraction.text.TfidfTransformer()
        tfs = tfidf.fit_transform(tokens);
        print tfs
        # index = Index(nltk.word_tokenize, 
        #       EnglishStemmer(), 
        #       nltk.corpus.stopwords.words('english'))
        # index.add(data.decode('utf-8').lower())
        # index.add(data.decode('utf-8').lower())
        # print index.index


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
        break