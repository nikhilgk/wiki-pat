# python mr_postings.py ../data/ten.tsv --output-dir=./postings  --no-output
import re
from mr_base import BaseMR
from mrjob.step import MRStep

class PostingsList(BaseMR):

    # OUTPUT_PROTOCOL=mrjob.protocol.PickleValueProtocol
    # OUTPUT_PROTOCOL=mrjob.protocol.JSONProtocol
    def configure_options(self):
        super(BaseMR, self).configure_options()

    def __init__(self, args):
        super(BaseMR, self).__init__(args)

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
        # yield token, sum(1 for _ in categories)
        yield token, len(set(categories))

    def reducer2(self, token, categories_sum):
        # yield token, sum(1 for _ in categories)
        yield token, sum(categories_sum)

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                    reducer=self.reducer),
            MRStep(reducer=self.reducer2)
        ]

if __name__ == '__main__':
    PostingsList.run()    
