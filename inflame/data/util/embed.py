"""
Chunk each document into words and then embed those words into 50D GloVe vectors.
Stack the embedded numeric document matrices into a numpy tensor (i.e. our predictors).
"""
from numpy import zeros
from gensim.utils import tokenize
from gensim.downloader import load
from functools import reduce

def pipe(*args):
   return reduce(lambda f, g: g(f), 
                 args
                )

class NLP:
   def __init__(self, docs):
      self.__DOCS = docs
      self.__FIXED_DOCSIZE = 200
      self.__WORD_VECS = load("glove-wiki-gigaword-50") ## Set an embedder that takes a text arg & embeds it.

   def _initialize(self):
      '''Make a 3d tensor initialized to 0s.
      '''
      dims = (len(self.__DOCS),   # number of docs
              self.__FIXED_DOCSIZE, 
              self.__WORD_VECS.vector_size    # embedding dimension
             )
      return zeros(dims)

   def _gen_tokens(self, text):
      '''Tokenize a text and keep only those tokens in the embedding space.
      '''
      return filter(lambda token: token in self.__WORD_VECS.vocab,
                    tokenize(text, lower=True)
                   )
      
   def _rm_stopwords(self, words: 'iterable'):
      '''Filter out stopwords.
      '''
      return filter(lambda word: word not in {'a', 'and', 'for', 'in', 'of', 'the', 'to'}, 
                    words
                   )
      
   def _trunc_doc(self, words: 'generator'):
      '''Keep only the first n words, where n is given by self.__FIXED_DOCSIZE.
      '''
      return list(words)[:self.__FIXED_DOCSIZE]

   def embed(self):
      '''The GloVe embedding.
      '''
      embedding = self._initialize()   # Prefills each tensor with 0's to ensure that all are the
                                       # same size regardless of text lengths.
      for i, doc in enumerate(self.__DOCS):
         words = pipe(doc, self._gen_tokens, self._rm_stopwords, self._trunc_doc)
         for j, word in enumerate(words):
            embedding[i, j] = self.__WORD_VECS[word]

      return embedding