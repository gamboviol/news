"""
train an LDA model on RCV1 data
"""

import sys
import logging
import math
import subprocess

from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamodel import LdaModel

from news.document import *

if len(sys.argv) != 2:
    print 'Usage: {0} rcv1_data_dir'.format(sys.argv[0])
    raise SystemExit(1)

data_dir = sys.argv[1]
mapping_file = data_dir+'/token_id_idf'
dictionary_file = data_dir+'/id_token_df'
token_file = data_dir+'/tokens'
lda_file = data_dir+'/lda_model'

print 'creating dictionary...'
N = 23307  # supplied idfs from rcv1/lyrl2004 were based on 23307 training docs
create_dictionary_file(mapping_file,dictionary_file,23307)
dictionary = Dictionary.load_from_text(dictionary_file)

print 'creating corpus...'
corpus = SimpleLowCorpus(token_file,dictionary)

print 'training model...'
logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
lda = LdaModel(corpus,id2word=dictionary,num_topics=200)
print 'done!'
print '\n'*3
print '======final topics======'
topics = lda.show_topics(topics=-1,topn=4)
for i,topic in enumerate(topics):
    print i,topic

print 'saving model...'
lda.save(lda_file)
