"""
Note: An n-gram is a sequence of n words.
In this training, we want to train based on n-grams.
We'll match each n-gram of encodings to the original
final word in the encoding

Example:
  string: "Hello there I am a robot"
  encoded string: "h3o t3e i a0m a r3t"
  3-gram 1: "h3o t3e i" --> i
  3-gram 2: "t3e i a0m" --> am
  3-gram 3: "i a0m a" --> a
  3-gram 4: "a0m a r3t" --> robot
"""

#! /usr/bin/env python
import sys
import re

PARSE_ALL_WORDS_RE_STRING = "([^\w\s]*\w(?:\d+\w)?[^\w\s]*|\S+|[\n\r\t\f]+)"
WORD_GROUPS_RE_STRING = "([^\w\s]*)(\w(?:\d+\w)?)([^\w\s]*)"

STATS = {}
N = 1 # overridden in __main__

# performs training for n = [1,2,3,...N]
def do_training(text):
  text = text.lower()
  words = re.findall("\w\S*\w|\w", text)
  for n in xrange(1,N+1): # [1,2,...,N]
    for i in xrange(len(words) + 1 - n):
      ngram_words = words[i:i+n]
      the_word = ngram_words[-1]
      encoded_ngram_words = []
      for word in ngram_words:
        if len(word) is 1:
          encoded_ngram_words.append(word)
        else:
          encoded_ngram_words.append(word[0] + str(len(word)-2) + word[-1])
      key = " ".join(encoded_ngram_words)

      if key not in STATS:
        STATS[key] = [[1, the_word]]
      else:
        poss_words = STATS[key]
        already_in_poss_words = False
        for poss_word_tuple in poss_words:
          if the_word == poss_word_tuple[1]:
            poss_word_tuple[0] += 1
            already_in_poss_words = True
            break
        if not already_in_poss_words:
          poss_words.append([1, the_word])

def read_file(file_name):
  with open(file_name, 'r') as f:
    return f.read()

# TODO: update this to work with ngrams
def decode(text):
  # note: encoded_words might include things that aren't words
  encoded_words = re.findall(PARSE_ALL_WORDS_RE_STRING, text)
  decoded_words = []

  # the first few words don't get picked up because 
  # we haven't reached a long enough ngram yet
  for i in xrange(N-1):
    leading_word = encoded_words[i]
    word_groups_match = re.match(WORD_GROUPS_RE_STRING, leading_word)
    if not word_groups_match:
      # the target word does not contain a real word
      if re.match("\w+", leading_word):
        # this is just whitespace
        decoded_words.append(leading_word)
      else:
        # this is just punctuation
        decoded_words.append(leading_word + " ")
    else:
      word_groups = word_groups_match.groups()
      leading = word_groups[0]
      trailing = word_groups[2]
      # just decodes it using a 1-gram. Whatever. Less code.
      the_decoded_word = decodeNGram(word_groups[1])
      decoded_word = leading + the_decoded_word + trailing + " "
      decoded_words.append(decoded_word)

  # Now the fun part :)
  for i in xrange(len(encoded_words)):
    encoded_ngram_words = encoded_words[i:i+N]
    the_encoded_word = encoded_ngram_words[-1]
    word_groups_match = re.match(WORD_GROUPS_RE_STRING, the_encoded_word)
    if not word_groups_match:
      # the target word does not contain a real word
      if re.match("\w+", the_encoded_word):
        # this is just whitespace
        decoded_words.append(the_encoded_word)
      else:
        # this is just punctuation
        decoded_words.append(the_encoded_word + " ")
    else:
      # the target contains a real word
      # First, prune the ngram to be only real words
      encoded_ngram_words = prune_to_real_word_list(encoded_ngram_words)
      encoding_ngram = " ".join(encoded_ngram_words)
      # note: encoding_ngram may be less than N elements
      # that's why we trained for all n in [1,2,...N]
      word_groups = word_groups_match.groups()
      leading = word_groups[0]
      trailing = word_groups[2]
      the_decoded_word = decodeNGram(encoding_ngram)
      decoded_word = leading + the_decoded_word + trailing + " "
      decoded_words.append(decoded_word)
  return "".join(decoded_words)

# encoding is an encoded ngram
def decodeNGram(encoding_ngram):
  if len(encoding_ngram) is 1:
    return encoding_ngram
  if encoding_ngram in STATS:
    return STATS[encoding_ngram][0][1]
  # if we reach here, we haven't encountered this 
  # encoding in the training. So we just fill the 
  # blanks with underscores
  last_word = encoding_ngram.split()[-1]
  num_between = int(last_word[1:-1])
  return last_word[0] + ("_"*num_between) + last_word[-1]

def prune_to_real_word_list(ngram):
  ret = []
  for super_word in ngram:
    word_groups_match = re.match(WORD_GROUPS_RE_STRING, super_word)
    if word_groups_match:
      word_groups = word_groups_match.groups()
      ret.append(word_groups[1])
  if len(ret) is 0:
    print "pruned the word list to be empty. whoops. ERROR!"
    quit(1)
  return ret



if __name__ == "__main__":
  if len(sys.argv) != 3:
    print "Expected a book title and a value for N (length of n-gram)!"
    quit(1)

  # Read in the encoded file
  title = sys.argv[1]
  title_file_name = "output_texts/{}.encoded.txt".format(title)
  full_encoded_text = read_file(title_file_name)

  # Train your algorithm!
  N = int(sys.argv[2])
  training_text_titles = ["frankenstein"]
  for training_title in training_text_titles:
    training_file_name = "original_texts/{}.full.txt".format(training_title)
    training_text = read_file(training_file_name)
    do_training(training_text)
  # After training, sort all the word counts in descending order to quickly get the max
  for key in STATS:
    STATS[key] = list(reversed(sorted(STATS[key])))
  print "Number of keys in training dictionary:", len(STATS.keys())
  # Decode the encoded file based on the training!
  decoded = decode(full_encoded_text)
  with open("output_texts/{}.decoded.{}.txt".format(title, N), 'w') as output_file:
    output_file.write(decoded)

  # Analyze our performance!
  full_original_file_name = "original_texts/{}.full.txt".format(title)
  full_original_text = read_file(full_original_file_name)
  original_words = full_original_text.split()
  decoded_words = decoded.split()

  num_original_words = len(original_words)
  num_decoded_words = len(decoded_words)
  if num_original_words != num_decoded_words:
    print "Error in analysis! Expected {} to equal {}".format(num_original_words, num_decoded_words)
    quit(1)
  num_correct = 0
  for i in xrange(num_original_words):
    original_word = original_words[i].lower()
    decoded_word = decoded_words[i].lower()
    if original_word == decoded_word:
      num_correct += 1
    else:
      print "Mismatch: '{}' != '{}'".format(original_word, decoded_word)
  print "Percent correct: {}%".format(num_correct*10000/num_original_words/100.)
