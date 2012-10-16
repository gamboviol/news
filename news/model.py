import threading
import logging

from gensim.models.ldamodel import LdaModel

from news.document import Tokenizer

class StoppableLdaModel(LdaModel):

    def __init__(self,dictionary,num_topics):
        LdaModel.__init__(self,id2word=dictionary,num_topics=num_topics)
        self.stop = False

    def do_mstep(self,rho,other):
        if self.stop:
            logging.info('stopping!')
            raise SystemExit(0)
        super(StoppableLdaModel,self).do_mstep(rho,other)

    def request_stop(self):
        logging.warn('stop requested... will abort training at the end of this batch')
        self.stop = True

class Model(object):

    def __init__(self,corpus,dictionary,num_topics,outfile):
        self.corpus = corpus
        self.outfile = outfile
        self.tokenizer = Tokenizer(dictionary)
        self.lda = StoppableLdaModel(dictionary,num_topics)
        self.training_thread = threading.Thread(target=self.train)
        self.training_thread.start()

    def train(self):
        logging.info('starting model training...')
        self.lda.update(self.corpus)
        self.lda.save(self.outfile)

    def topics(self,text):
        bow = self.tokenizer.text2bow(text)
        return str(self.lda[bow])

    def show_topic(self,topic,topn=10):
        return str(self.lda.show_topic(topic,topn=topn))

    def print_topic(self,topic,topn=10):
        return self.lda.print_topic(topic,topn=topn)

    def request_stop(self):
        self.lda.request_stop()
        return 'stopping'
