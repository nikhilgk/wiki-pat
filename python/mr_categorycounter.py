# python mr_categories.py ../data/ten.tsv --output-dir=./categories  --no-output
import re
from mr_base import BaseMR

class CategoryCounter(BaseMR):

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
        for category in categories:
            yield 'A', category  

    def reducer(self, token, categories):
        count = len(set(categories))
        yield 'count', count

    # def mapper(self, line_no, line):
    #     data = line.split('\t')
    #     categories = self.doctocats(data)
    #     for category in categories:
    #         yield category, 1  

    # def reducer(self, category, counter):
    #     count = sum(1 for _ in counter)
    #     yield category, count

if __name__ == '__main__':
    CategoryCounter.run()    
