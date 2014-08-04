# sudo apt-get install python-numpy python-scipy
# sudo apt-get install python-dev
# sudo apt-get install libatlas-base-dev gfortran

import os
import sys
import csv
import re
import os
import math
from xml.etree import ElementTree
import nltk
from nltk.corpus import XMLCorpusReader
from nltk.corpus import WordListCorpusReader

from nltk.tokenize import line_tokenize 
from collections import defaultdict
from nltk.stem.snowball import EnglishStemmer
import sklearn

csv.field_size_limit(sys.maxsize)

tsv = open("../data/ten.tsv")
for line in csv.reader(tsv, dialect="excel-tab"): #You can also use delimiter="\t" rather than giving a dialect.
    xml = line[3]
    result = re.finditer('(Category:[^<]*)', xml)
    categories = [m.group(0).replace('Category:','') for m in result]
    print categories
    # metadata_store.add(count, line[1], categories)
    # print line[1]
    
