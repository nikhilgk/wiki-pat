# -*- coding: ascii -*-
from collections import Counter
from collections import defaultdict
from operator import itemgetter
import nltk
from nltk.stem.lancaster import LancasterStemmer
import sys
import math
import re
import collections

class Classifier:

    def __init__(self, index_file, postings_file,category_count_file):
        self.stopwords = set(nltk.corpus.stopwords.words('english'))
        self.stemmer = LancasterStemmer()
        self.index_file = index_file


        #Loading the compressed postings file
        self.postings_list = {}
        postings_reader = open(postings_file)
        for line in postings_reader:
            parts = line.split('\t')
            self.postings_list[eval(parts[0])] = eval(parts[1].strip())
        # print self.postings_list
        print "Done reading postings list"

        #Loading the number of categories
        count_reader = open(category_count_file)
        line = count_reader.readline()
        parts = line.split('\t')
        self.category_count = eval(parts[1].strip())
        print "Done reading category count :" + str(self.category_count)



    def transform(self, word):
        word = word.lower()
        if self.stemmer:
                try:
                        word = self.stemmer.stem(word)
                except:
                        return word
        return word

    def idf(self, term):
        # term = self.transform(term).encode('ascii', 'ignore')
        if term in self.postings_list:
             return math.log(self.category_count * 1.0 / self.postings_list[term])
        else:
             return 0

    def tfidf(self, tf):
        # for word in tf:
        #     print self.idf(word) 
        return {word: tf[word] * self.idf(word) for word in tf}


    def document_tf(self, document):
        pattern = re.compile('[a-zA-Z_]+')
        document = document.decode('ascii',errors='ignore').lower()
        tokens = set(re.findall(pattern, document))
        tf = {}
        for token in tokens:
            # print tokensoken
            if token in self.stopwords:
                    continue
            token = self.transform(token)
            # print token
            if token in tf:
                    tf[token] += 1
            else:
                    tf[token] = 1
        return tf

    def cosine_similarity(self, cat_vector, query_vector, query_tf):
        num = 0
        sum1 = sum([float(cat_vector[x]) * float(cat_vector[x]) for x in cat_vector])
        sum2 = sum([float(query_vector[x]) * float(query_vector[x]) for x in query_vector])
        cat_vector = defaultdict((lambda: 0), cat_vector)
        query_vector = defaultdict((lambda: 0), query_vector)
        num = sum([float(cat_vector[term]) * query_vector[term] for term in query_tf])
        return num * 1.0 / math.sqrt(sum1 * sum2)

    def classify(self, document):
        query_tf = self.document_tf(document)
        query_tfidf = self.tfidf(query_tf)

        scores = {}
        index = open(self.index_file)
        for item in index:
            parts = item.split('\t')
            cat = eval(parts[0])
            cat_tfidf = eval(parts[1].strip())

            score = self.cosine_similarity(cat_tfidf, query_tfidf, query_tf)
            scores[cat] = score

        scores  = collections.OrderedDict(sorted(scores.items(), key=lambda t: t[1], reverse=True))  

        return scores

classifier = Classifier(sys.argv[1], sys.argv[2], sys.argv[3])
scores = classifier.classify('Following World War II, Alabama experienced growth as the economy of the state transitioned from one primarily based on agriculture to one with diversified interests. The establishment or expansion of multiple United States Armed Forces installations added to the state economy and helped bridge the gap between an agricultural and industrial economy during the mid-20th century. The state economy in the 21st century is dependent on management, automotive, finance, manufacturing, aerospace, mineral extraction, healthcare, education, retail, and technology')
# scores = classifier.classify('In computing, C as in the letter C) is a general-purpose programming language initially developed by Dennis Ritchie between 1969 and 1973 at AT&T Bell Labs.[5][6] Like most imperative languages in the ALGOL tradition, C has facilities for structured programming and allows lexical variable scope and recursion, while a static type system prevents many unintended operations. Its design provides constructs that map efficiently to typical machine instructions, and therefore it has found lasting use in applications that had formerly been coded in assembly language, most notably system software like the Unix computer operating system.[7]                  C is one of the most widely used programming languages of all time,[8][9] and C compilers are available for the majority of available computer architectures and operating systems.                  Many later languages have borrowed directly or indirectly from C, including D, Go, Rust, Java, JavaScript, Limbo, LPC, C#, Objective-C, Perl, PHP, Python, Verilog (hardware description language),[4] and Unix"        s C shell. These languages have drawn many of their control structures and other basic features from C. Most of them (with Python being the most dramatic exception) are also very syntactically similar to C in general, and they tend to combine the recognizable expression and statement syntax of C with underlying type systems, data models, and semantics that can be radically different. C++ and Objective-C started as compilers that generated C code; C++ is currently nearly a superset of C,[10] while Objective-C is a strict superset of C.')


count=0
for k,v in scores.items():
    print k, ' : ', v
    count += 1
    if count == 5:
        break 

# print sco