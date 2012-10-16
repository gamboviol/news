"""
query an LDA model on RCV1 data while it trains continuously
-- server code
"""

import logging
from SimpleXMLRPCServer import SimpleXMLRPCServer

from gensim.corpora.dictionary import Dictionary

from news.document import *
from news.model import *

class ModelServer(SimpleXMLRPCServer):

    def __init__(self,model,host,port):
        SimpleXMLRPCServer.__init__(self,(host,port))
        self.model = model

    def _dispatch(self,method,params):
        try:
            func = getattr(self,method)
        except AttributeError:
            try:
                func = getattr(self.model,method)
            except AttributeError:
                raise Exception('method "{0}" is not supported'.format(method))
        return func(*params)

    def serve_forever(self):
        self.quit = False
        logging.info('starting server...')
        while not self.quit:
            self.handle_request()

    def stop(self):
        self.quit = True
        logging.info('requesting model to stop training...')
        self.model.request_stop()
        return 'ok'

if __name__ == '__main__':

    import sys

    if len(sys.argv) != 2:
        print 'Usage: {0} rcv1_data_dir'.format(sys.argv[0])
        raise SystemExit(1)

    data_dir = sys.argv[1]
    mapping_file = data_dir+'/token_id_idf'
    dictionary_file = data_dir+'/id_token_df'
    token_file = data_dir+'/tokens'
    lda_file = data_dir+'/lda_model'

    logging.basicConfig(format='%(levelname)s : %(message)s',level=logging.INFO)

    logging.info('creating dictionary...')
    N = 23307  # supplied idfs from rcv1/lyrl2004 were based on 23307 training docs
    create_dictionary_file(mapping_file,dictionary_file,23307)
    dictionary = Dictionary.load_from_text(dictionary_file)

    logging.info('creating corpus...')
    corpus = SimpleLowCorpus(token_file,dictionary)

    num_topics = 200
    model = Model(corpus,dictionary,num_topics,lda_file)

    server = ModelServer(model,'localhost',8000)
    server.serve_forever()
