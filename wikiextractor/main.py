import os
from xml.etree import ElementTree
import nltk
from nltk.corpus import XMLCorpusReader
from nltk.corpus import WordListCorpusReader

from nltk.tokenize import line_tokenize 

tree =  ElementTree.parse("/home/nikhil/ws/mids/w205/project/AA/wiki_00")
root = tree.getroot()
count = 0
#Iterate through all the Pages
for child in root:
    # print child.text
    # wordlists = XMLCorpusReader('/home/nikhil/ws/mids/w205/project/AA', 'wiki_00')
    # print wordlists.words()
    tokens = nltk.word_tokenize(child.text.encode('utf-8').lower())
    text = nltk.Text(tokens)
    text.collocations()
    print '---------------------'
    # break
   