import csv
import nltk
import sys
from collections import defaultdict
from nltk.stem.snowball import EnglishStemmer
from mrjob.job import MRJob

class WordCounter(MRJob):
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
    
    def mapper_tokenize(self, line_no, line):
        data = line.split('\t')
        document = data[4].decode('utf-8').lower().replace('\\n', '\n')
        for token in [t.lower() for t in nltk.word_tokenize(document)]:
            if token in self.stopwords:
                continue
            token = self.transform(token)
            yield token, 1    
 
    def combiner_tokenize(self, word, counts):
        yield (word, sum(counts))
 
    def reducer_tokenize(self, word, counts):
        yield (None, 1)

    def reducer_word_count(self, _, word_count):
        # each item of word_count_pairs is (count, word),
        # so yielding one results in key=counts, value=word
        print '#######################'
        wc = sum(word_count)
        print wc
        yield (None, wc)


    def steps(self):
        return [
            self.mr(mapper=self.mapper_tokenize,
                    combiner=self.combiner_tokenize,
                    reducer=self.reducer_tokenize),
            self.mr(reducer=self.reducer_word_count)
        ]
        
if __name__ == '__main__':
    WordCounter.run()    
