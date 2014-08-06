from collections import Counter
from collections import defaultdict
from operator import itemgetter
import nltk
from nltk.stem.snowball import EnglishStemmer
import sys
import math

class Classifier:

    def __init__(self, terms_file, postings_file, categories_file):
        self.terms = {}
        self.postings_list = {}
        self.categories = {}
        self.stopwords = set(nltk.corpus.stopwords.words('english'))
        self.stemmer = EnglishStemmer()

        #Parse terms file
        terms_reader = open(terms_file)
        for line in terms_reader:
                parts = line.split('\t')
                self.terms[eval(parts[0])] = eval(parts[1].strip())
        print "Done reading terms"
        
        #Parse postings lists
        postings_reader = open(postings_file)
        for line in postings_reader:
                parts = line.split('\t')
                self.postings_list[eval(parts[0])] = eval(parts[1].strip())
        print "Done reading postings list"

        #Parse categories
        categories_reader = open(categories_file)
        for line in categories_reader:
                parts = line.split('\t')
                self.categories[eval(parts[0])] = eval(parts[1].strip())
        print "Done reading categories list"

        self.numDocs = len(self.terms)

    def transform(self, word):
        word = word.lower()
        if self.stemmer:
                try:
                        word = self.stemmer.stem(word)
                except:
                        return word
        return word

    def idf(self, term):
        term = self.transform(term).encode('ascii', 'ignore')
        if term in self.postings_list:
                return math.log(self.numDocs * 1.0 / len(self.postings_list[term]))
        else:
                return 0

    def tfidf(self, tf):
        return {word: tf[word] * self.idf(word) for word in tf}

    def category_tf(self, category):
        if category not in self.categories:
                return {}
        docs = self.categories[category]
        tf = {}
        doc_tfs = [self.terms[doc] for doc in docs if doc in self.terms]
        return sum((Counter(x) for x in doc_tfs), Counter())

    def category_tfidf(self, category):
        return self.tfidf(self.category_tf(category))

    def document_tf(self, document):
        document = document.decode('utf-8').lower().replace('\\n', '\n')
        tf = {}
        for token in [t.lower() for t in nltk.word_tokenize(document)]:
                if token in self.stopwords:
                        continue
                token = self.transform(token)
                if token in tf:
                        tf[token] += 1
                else:
                        tf[token] = 1
        return tf

    def cosine_similarity(self, vector1, vector2):
        num = 0
        sum1 = sum([vector1[x] * vector1[x] for x in vector1])
        sum2 = sum([vector2[x] * vector2[x] for x in vector2])
        vector1 = defaultdict((lambda: 0), vector1)
        vector2 = defaultdict((lambda: 0), vector2)
        num = sum([vector1[term] * vector2[term] for term in self.postings_list])
        return num * 1.0 / math.sqrt(sum1 * sum2)

    def classify(self, document):
        tf = self.document_tf(document)
        test_tfidf = self.tfidf(tf)
        category_tfidfs = [(x, self.category_tfidf(x)) for x in self.categories]
        scores = [(x[0], self.cosine_similarity(x[1], test_tfidf)) for x in category_tfidfs]
        scores = sorted(scores, key=itemgetter(1), reverse=True)
        return scores

classifier = Classifier(sys.argv[1], sys.argv[2], sys.argv[3])
print len(classifier.terms), len(classifier.postings_list), len(classifier.categories)
print classifier.idf('country')
scores = classifier.classify('Following World War II, Alabama experienced growth as the economy of the state transitioned from one primarily based on agriculture to one with diversified interests. The establishment or expansion of multiple United States Armed Forces installations added to the state economy and helped bridge the gap between an agricultural and industrial economy during the mid-20th century. The state economy in the 21st century is dependent on management, automotive, finance, manufacturing, aerospace, mineral extraction, healthcare, education, retail, and technology')

print scores[0:5]
