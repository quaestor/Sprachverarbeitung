import os

from nltk.corpus.reader import *
from nltk.tokenize import *

from nltk.corpus.reader.api import *
from nltk.corpus.reader.util import *

class SvTaggedcorpusReader(TaggedCorpusReader):

	def __init__(self, root, fileids, tagset='tagset',
			sep='/', word_tokenizer=WhitespaceTokenizer(),
			sent_tokenizer=RegexpTokenizer('\n', gaps=True),
			para_block_reader=read_blankline_block,
			encoding=None,
			tag_mapping_function=None):
		TaggedCorpusReader.__init__(self, root, fileids, encoding)
		self._sep = sep
		self._word_tokenizer = word_tokenizer
		self._sent_tokenizer = sent_tokenizer
		self._para_block_reader = para_block_reader
		self._tag_mapping_function = tag_mapping_function
		self._tagset = dict([line.split('\t') for line in self.open('tagset').read().splitlines()])

	def tagset(self):
		return self._tagset
