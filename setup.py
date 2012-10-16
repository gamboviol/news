from setuptools import setup

setup(packages=['news'],
      version='0.0.1',
      maintainer='Mark Levy',
      name='news',
      package_dir={'': '.'},
      description='news topic modelling',
      install_requires=['gensim>=0.8.6','nltk'])
