# vim: set fileencoding=utf-8 :
from __future__		import division
import nltk
import re
from random		import randint
from nltk.corpus	import wordnet as wn

def ngrams(n, text):
	return [tuple(text[i:i+n]) for i in range(0,len(text)-n)]

def max_ngram(xs):
	return FreqDist(xs).items()[0]

def generate_model(cfdist, word, num=15): 
	for i in range(num): 
		print word, 
		if (i % 2 == 0):
			word = cfdist[word].max()

		else:
			word = cfdist[word].keys()[-1]

def generalize(sentence):
	newsent = []
	for word in nltk.word_tokenize(sentence):
		if(wn.synsets(word) != []):
			dis = disambiguateWordSenses(sentence,word)
			if(dis):
				hyp = hypernyms()
			if(hyp != []):
				newsent.append(hyp[0].lemma_names[0])
			else:
				newsent.append(word)
	return newsent

def word_similarity(word1, word2):
   w1synsets = wn.synsets(word1)
   w2synsets = wn.synsets(word2)
   maxsim = 0
   for w1s in w1synsets:
       for w2s in w2synsets:
           current = wn.path_similarity(w1s, w2s)
           if (current > maxsim and current > 0):
               maxsim = current
           #print "Common hypernyms of ", w1s, " and ", w2s, ": ", w1s.common_hypernyms(w2s)
   return maxsim

def disambiguateWordSenses(sentence, word):
   wordsynsets = wn.synsets(word)
   bestScore = 0.0
   result = None
   for synset in wordsynsets:
       for w in nltk.word_tokenize(sentence):
           score = 0.0
           for wsynset in wn.synsets(w):
               sim = wn.path_similarity(wsynset, synset)
               if(sim == None):
                   continue
               else:
                   score += sim
           if (score > bestScore):
              bestScore = score
              result = synset
   return result

def antonymize(sent):
	nsent = []
	for word in sent:
		synsets = wn.synsets(word);
		if(synsets == []):
			nsent.append(word)
			continue
		antonym = [synset.lemmas[0].antonyms() for synset in synsets if
				synset.lemmas[0].antonyms() != []]
		if(antonym == []):
			nsent.append(word)
			continue
		nsent.append(antonym[0][0].name)
	return nsent 

def segment(text, segs):
	words = []
	last = 0
	for i in range(len(segs)):
		if segs[i] == '1':
			words.append(text[last:i+1])
			last = i+1
	words.append(text[last:])
	return words

def evaluate(text, segs):
	words = segment(text, segs)
	text_size = len(words)
	lexicon_size = len(' '.join(list(set(words))))
	return text_size + lexicon_size

def flip(segs, pos):
	return segs[:pos] + str(1-int(segs[pos])) + segs[pos+1:]

def flip_n(segs, n):
	for i in range(n):
		segs = flip(segs, randint(0,len(segs)-1))
	return segs

def anneal(text, segs, iterations, cooling_rate):
	temperature = float(len(segs))
	while temperature > 0.5:
		best_segs, best = segs, evaluate(text, segs)
		for i in range(iterations):
			guess = flip_n(segs, int(round(temperature)))
			score = evaluate(text, guess)
			if score < best:
				best, best_segs = score, guess
		score, segs = best, best_segs
		temperature = temperature / cooling_rate
		print evaluate(text, segs), segment(text, segs)
	print
	return segs

def read_tagged_text(text):
	return map(lambda t: re.split(r'/', t), re.split(r'[ \n]+', text))

def load_tiger_corpus(path=None):
	if(path == None):
		path = nltk.data.find('corpora/tigercorpus')
	return nltk.corpus.TaggedCorpusReader(path, 'tc', encoding='utf-8')

def rate_tagged(guess, golden):
	return sum([guess[i] == golden[i] for i in range(0,len(guess))]) / len(guess) * 100

def reg_tag(words, patterns):
	regexp_tagger = nltk.RegexpTagger(patterns)
	return regexp_tagger.tag(words)

def pattern_german_nouns(corpus, tag):
	tag_words = [w[0] for w in corpus.tagged_words() if w[1] == tag]
	start = sorted(set([w[:3] for w in tag_words if w.isalpha() and w[1:3].islower() and len(w) >= 3]))
	ending = sorted(set([w[:3] for w in tag_words if w.isalpha() and w.islower() and len(w) >= 3]))
	return '^(' + '|'.join(start) + ').*(' + '|'.join(end) + ')$'


