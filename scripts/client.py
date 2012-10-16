"""
query an LDA model on RCV1 data while it trains continuously
-- client code
"""

import xmlrpclib
from operator import itemgetter

model = xmlrpclib.ServerProxy('http://localhost:8000')

while True:
    text = raw_input('enter text (q to quit): ')
    if text == 'q':
        print 'requesting server shutdown'
        model.stop()
        print 'bye!'
        break
    topics = eval(model.topics(text))
    for topic,weight in sorted(topics,key=itemgetter(1),reverse=True):
        terms = [term for _,term in eval(model.show_topic(topic,4))]
        print '{0} (weight {1:.3})'.format(', '.join(terms),weight)
