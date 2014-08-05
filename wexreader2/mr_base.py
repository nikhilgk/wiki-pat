import nltk
from nltk.stem.lancaster import LancasterStemmer

import re, string
import types

from mrjob.job import MRJob

class BaseMR(MRJob):
    stemmer = LancasterStemmer()
    stopwords = set(nltk.corpus.stopwords.words('english'))
    pattern = re.compile('[a-zA-Z_]+')

    def __init__(self, args):
        super(BaseMR, self).load_options(args)

    def transform(self, word):
        word = word.lower()
        if self.stemmer:
            try:
                    word = self.stemmer.stem(word)
            except:
                return word
        return word
        
    def tokenize(self, data, yielder):
        print data[1]
        article = data[4].decode('ascii',errors='ignore').lower()
        # document = self.pattern.sub('',data[4].decode('ascii',errors='ignore').lower().replace('\\n', '\n'))
        tokens = set(re.findall(self.pattern, article))
        # for token in [t.lower() for t in nltk.word_tokenize(document)]:
        for token in tokens:
            if token in self.stopwords:
                continue
            token = self.transform(token)
            resp = yielder(token)
            if isinstance(resp, list):
                for item in resp: yield item
            else:
                yield resp
            