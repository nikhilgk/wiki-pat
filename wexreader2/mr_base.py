import nltk
from nltk.stem.lancaster import LancasterStemmer

import re, string
import types
from nltk.collocations import *
from nltk.metrics import BigramAssocMeasures

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
    
    counter = 0
    def tokenize(self, data, yielder):
        self.counter += 1
        print str(self.counter)+' : ' + data[1]
        article = data[4].decode('ascii',errors='ignore').lower()
        # tokens = nltk.word_tokenize(article)
        tokens = re.findall(self.pattern, article)

        #Handle Bigrams
        num=20
        window_size=2
        finder = BigramCollocationFinder.from_words(tokens, window_size)
        finder.apply_freq_filter(2)
        finder.apply_word_filter(lambda w: len(w) < 3 or w.lower() in self.stopwords)
        bigram_measures = BigramAssocMeasures()
        _collocations = finder.nbest(bigram_measures.likelihood_ratio, num)
        colloc_strings = [w1+' '+w2 for w1, w2 in _collocations]
        for colloc in colloc_strings:
            resp = yielder(colloc)
            if isinstance(resp, list):
                for item in resp: yield item
            else:
                yield resp

        #Handle individual tokens
        tokens=set(tokens)
        uniquetokens = set()
        for token in tokens:
            if token in self.stopwords:
                continue
            token = self.transform(token)
            uniquetokens.add(token)
        for token in uniquetokens:
            resp = yielder(token)
            if isinstance(resp, list):
                for item in resp: yield item
            else:
                yield resp
            


    #             tokens = nltk.word_tokenize(child.text.encode('utf-8').lower())
    # text = nltk.Text(tokens)
    # text.collocations()