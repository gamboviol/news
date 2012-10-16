import math
import subprocess

from nltk.stem import *

def create_dictionary_file(mapping_file,dictionary_file,N):
    f = open(mapping_file)
    g = open(dictionary_file,'wb')
    for line in f:
        token,id,idf = line.strip().split()
        id = int(id)
        idf = float(idf)
        df = int(round(N/math.exp(idf)))
        print >>g,'{0}\t{1}\t{2}'.format(id,token,df)

class SimpleLowCorpus(object):

    def __init__(self,token_file,dictionary):
        """
        token_file is space separated docID token token token ...
        """
        self.token_file = token_file
        self.dictionary = dictionary
        self.len = int(subprocess.check_output(['wc','-l',token_file]).split()[0])

    def __iter__(self):
        f = open(self.token_file)
        for line in f:
            yield self.dictionary.doc2bow(line.split()[1:])

    def __len__(self):
        return self.len

class Tokenizer(object):

    def __init__(self,dictionary):
        self.dictionary = dictionary
        self.stemmer = PorterStemmer()

    def text2bow(self,text):
        stemmed_text = [self.stemmer.stem(w) for w in text.strip().lower().split()]
        return self.dictionary.doc2bow(stemmed_text)
