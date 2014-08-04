# python mr_terms.py ../data/ten.tsv --output-dir=./terms
import re, sys
from mr_base import BaseMR

class TermsList(BaseMR):

    def configure_options(self):
        super(TermsList, self).configure_options()
        self.add_passthrough_option('--postings_file')

    def __init__(self, args):
        super(TermsList, self).__init__(args)
        postings_file = self.options.postings_file
        print postings_file
        self.postings_list = {}
        postings_reader = open(postings_file)
        for line in postings_reader:
            parts = line.split('\t')
            self.postings_list[eval(parts[0])] = eval(parts[1].strip())
        print "Done reading postings list"

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
        # print self.postings_list
        index = {}
        for token in tokens:
            if token in index:
                index[token] += 1
            else:
                index[token] = 1
        yield category, index

if __name__ == '__main__':
    TermsList.run()    
