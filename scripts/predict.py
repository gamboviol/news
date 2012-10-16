"""
make simple topic predictions from a saved LDA model
"""

import sys
from operator import itemgetter

from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamodel import LdaModel

from news.document import Tokenizer

if len(sys.argv) != 2:
    print 'Usage: {0} rcv1_data_dir'.format(sys.argv[0])
    raise SystemExit(1)

data_dir = sys.argv[1]
dictionary_file = data_dir+'/id_token_df'
model_file = data_dir+'/lda_model'

print 'creating tokenizer...'
dictionary = Dictionary.load_from_text(dictionary_file)
tok = Tokenizer(dictionary)

print 'loading model...'
lda = LdaModel.load(model_file)

while True:
    text = raw_input('enter text (q to quit): ')
    if text == 'q':
        print 'bye!'
        break
    doc = tok.text2bow(text)
    topics = lda[doc]
    for topic,weight in sorted(topics,key=itemgetter(1),reverse=True):
        print weight,lda.show_topic(topic,topn=4)
