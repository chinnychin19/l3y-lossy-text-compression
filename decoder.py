#! /usr/bin/env python
import sys
import re

PARSE_ALL_WORDS_RE_STRING = "([^\w\s]*\w(?:\d+\w)?[^\w\s]*|\S+|[\n\r\t\f]+)"
WORD_GROUPS_RE_STRING = "([^\w\s]*)(\w(?:\d+\w)?)([^\w\s]*)"

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

def decodeWord(word): # TODO
  if len(word) is 1:
    return word
  # TODO: return a guess
  num_between = int(word[1:-1])
  return word[0] + ("_"*num_between) + word[-1]

def containsARealWord(word):
  return re.match(CONTAINS_WORD_RE_STRING, word) is not None

def leadingPunctuation(word):
  m = LEADING_PUNCTUATION_RE.search(word)
  if m is None:
    return None
  return m.group(0) # the whole match

def trailingPunctuation(word):
  m = TRAILING_PUNCTUATION_RE.search(word)
  if m is None:
    return None
  return m.group(0) # the whole match

def stripWord(word):
  m = STRIP_WORD_RE.search(word)
  if m is None:
    return None
  return m.group(1) # the match between leading and trailing punctuation


if __name__ == "__main__":
  if len(sys.argv) != 2:
    print "Expected a single book title!"
    quit(1)

  title = sys.argv[1]
  title_file_name = "output_texts/{}.encoded.txt".format(title)
  full_text = read_file(title_file_name)
  decoded = decode(full_text)
  with open("output_texts/{}.decoded.txt".format(title), 'w') as output_file:
    output_file.write(decoded)
