# python mr_postings.py ../data/ten.tsv --output-dir=./postings
import re
from mr_base import BaseMR

class PostingsList(BaseMR):

    # OUTPUT_PROTOCOL=mrjob.protocol.PickleValueProtocol
    # OUTPUT_PROTOCOL=mrjob.protocol.JSONProtocol

    def doctocats(self, data):
        xml = data[3]
        result = re.finditer('(Category:[^<]*)', xml)
        categories = [m.group(0).replace('Category:','') for m in result]        
        return categories
    
    def mapper(self, line_no, line):
        data = line.split('\t')
        categories = self.doctocats(data)
        def yielder (token):
            return [[token, category] for category in categories]
        return self.tokenize(data, yielder)  

    def reducer(self, token, categories):
        yield token, sum(1 for _ in categories)


if __name__ == '__main__':
    PostingsList.run()    
