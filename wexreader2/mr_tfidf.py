# python mr_tfidf.py.py ../data/ten.tsv --output-dir=./terms --postings_file=./postings/part-00000 --no-output --category_count=./categories/part-00000 
import re, sys
import math
from mr_base import BaseMR
import mrjob
import collections

class TermsList(BaseMR):

    # OUTPUT_PROTOCOL=mrjob.protocol.PickleValueProtocol
    def configure_options(self):
        super(BaseMR, self).configure_options()
        self.add_passthrough_option('--postings_file')
        self.add_passthrough_option('--category_count')

    def __init__(self, args):
        super(BaseMR, self).__init__(args)

        #Loading the compressed postings file
        postings_file = self.options.postings_file
        self.postings_list = {}
        postings_reader = open(postings_file)
        for line in postings_reader:
            parts = line.split('\t')
            self.postings_list[eval(parts[0])] = eval(parts[1].strip())
        print "Done reading postings list"

        #Loading the number of categories
        category_count_file = self.options.category_count
        count_reader = open(category_count_file)
        line = count_reader.readline()
        parts = line.split('\t')
        self.category_count = eval(parts[1].strip())
        print "Done reading category count :" + str(self.category_count)


    def doctocats(self, data):
        xml = data[3]
        result = re.finditer('(Category:[^<]*)', xml)
        categories = [m.group(0).replace('Category:','') for m in result]        
        return categories
    
    def mapper(self, line_no, line):
        data = line.split('\t')
        categories = self.doctocats(data)
        def yielder (token):
            # return 1,1
            return [[category, token] for category in categories]
        return self.tokenize(data, yielder)  

    def reducer(self, category, tokens):
        index = {}

        for token in tokens:
            if token in index:
                index[token] += 1
            else:
                index[token] = 1
        tfidfs = {}
        for token in self.postings_list:
            if token in index:
                idf = math.log(self.category_count * 1.0 / self.postings_list[token])
                tf = index[token] 
                tfidf = tf * idf
                tfidfs[token] = tfidf
                # tfidfs[token] = "{0:.2f}".format(tfidf)
        #Sort the dictionary by the tfidf
        tfidfs  = collections.OrderedDict(sorted(tfidfs.items(), key=lambda t: t[1], reverse=True))        
        
        # 10% of items or atleast 10 items
        count=max( int(len(tfidfs)*0.1), 10) 
        filtererd_tfidfs = {}
        for k,v in tfidfs.items():
            # print k, ' : ', v
            filtererd_tfidfs[k]=v
            count -= 1
            if count == 0:
                break 

        yield category, filtererd_tfidfs

if __name__ == '__main__':
    TermsList.run()    

import itertools

dict(itertools.islice(dict2.iteritems(), 0, 5)) 