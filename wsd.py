import nltk
from nltk.corpus import wordnet as wn

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

# disambiguateWordSenses('sitting on a bank', 'bank')
# wn.synset('bank.n.01').definition
