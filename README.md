news
====

topic modelling for news items

installation
------------

prerequisites:

* gensim
* nltk

to install this module and prerequisites should just need:

	python setup.py install

running
-------

1. download some (large) data files, known as the RCV1 dataset, which consists of just over 800,000 Reuters news stories from 1996-7, mainly about topics of business interest:

		./scripts/get_data.sh

   This will create and populate an rcv1/ directory.

2. start up a server which trains a topic model on the RCV1 news items:

		python scripts/server.py rcv1

3. as soon as training has started, start up a client which queries the server for learned topics matching any text that you enter:

		python scripts/client.py

   The top few terms for each matching topic will be displayed.  Note that you'll actually see *stemmed* text tokens, i.e. partial words stripped of their endings, for each topic, as that's what the dataset contains.  You should see sensible topics as long as the text you enter has some similarity with the items in the dataset.  Obviously if you enter just a few words, or a sentence where none of the words ever appeared in the business papers in 1996-7, then all bets are off.

   Although you can query the model right away, you should notice that the topics change (hopefully for the better) if you re-enter the same news item after a few more learning iterations.

background
----------

As this project demonstrates, topic modelling, i.e. learning underlying topics automatically from text documents, is now a fairly mature field, and fast implementations of a number of standard models are easily available, including parallel implementations to deal with huge numbers of documents.

The implementation used here is "online" in the sense that documents can be streamed for learning and don't all have to be held in memory, hence it can process a large number of documents in a short time.  The model learned is not itself truly "online" i.e. it doesn't adapt fully to new data once it has already seen a reasonable number of documents.  However the quick training time means that simple strategies can be used to refresh or replace models in order to keep them well fitted to news stories as the underlying topics change over time.
