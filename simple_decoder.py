#! /usr/bin/env python
import sys
import re

PARSE_ALL_WORDS_RE_STRING = "([^\w\s]*\w(?:\d+\w)?[^\w\s]*|\S+|[\n\r\t\f]+)"
WORD_GROUPS_RE_STRING = "([^\w\s]*)(\w(?:\d+\w)?)([^\w\s]*)"

STATS = {}

def do_training(text):
  text = text.lower()
  words = re.findall("\w\S*\w|\w", text)
  for word in words:
    encoding = ""
    if len(word) is 1:
      encoding = word
    else:
      encoding = word[0] + str(len(word)-2) + word[-1]

    if encoding not in STATS:
      STATS[encoding] = [[1, word]]
    else:
      poss_words = STATS[encoding]
      already_in_poss_words = False
      for poss_word_tuple in poss_words:
        if word == poss_word_tuple[1]:
          poss_word_tuple[0] += 1
          already_in_poss_words = True
          break
      if not already_in_poss_words:
        poss_words.append([1, word])

def read_file(file_name):
  with open(file_name, 'r') as f:
    return f.read()

def decode(text):
  encoded_words = re.findall(PARSE_ALL_WORDS_RE_STRING, text)
  decoded_words = []
  for encoded_word in encoded_words:
    word_groups_match = re.match(WORD_GROUPS_RE_STRING, encoded_word)
    if word_groups_match is not None:
      word_groups = word_groups_match.groups()
      leading = word_groups[0]
      the_word = word_groups[1]
      trailing = word_groups[2]
      decoded_word = leading + decodeWord(the_word) + trailing + " "
      decoded_words.append(decoded_word)
    else:
      if re.match("\w+", encoded_word):
        # this is whitespace
        decoded_words.append(encoded_word)
      else:
        # this is punctuation
        decoded_words.append(encoded_word + " ")
  return "".join(decoded_words)

def decodeWord(encoding):
  if len(encoding) is 1:
    return encoding
  if encoding in STATS:
    return STATS[encoding][0][1]
  # if we reach here, we haven't encountered this 
  # encoding in the training. So we just fill the 
  # blanks with underscores
  num_between = int(encoding[1:-1])
  return encoding[0] + ("_"*num_between) + encoding[-1]


if __name__ == "__main__":
  if len(sys.argv) != 2:
    print "Expected a single book title!"
    quit(1)

  # Read in the encoded file
  title = sys.argv[1]
  title_file_name = "output_texts/{}.encoded.txt".format(title)
  full_encoded_text = read_file(title_file_name)

  # Train your algorithm!
  training_text_titles = ["frankenstein"]
  for training_title in training_text_titles:
    training_file_name = "original_texts/{}.full.txt".format(training_title)
    training_text = read_file(training_file_name)
    do_training(training_text)
  # After training, sort all the word counts in descending order to quickly get the max
  for key in STATS:
    STATS[key] = list(reversed(sorted(STATS[key])))

  # Decode the encoded file based on the training!
  decoded = decode(full_encoded_text)
  with open("output_texts/{}.decoded.txt".format(title), 'w') as output_file:
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
