#! /usr/bin/env python
import sys
import re

LEADING_PUNCTUATION_RE = re.compile("^\W+")
TRAILING_PUNCTUATION_RE = re.compile("\W+$")
STRIP_WORD_RE = re.compile("^\W*(.*?)\W*$")

def read_file(file_name):
  with open(file_name, 'r') as f:
    return f.read()

def encode(text):
  encoded_words = []
  words = re.findall("(\S+|[\n\r\t\f]+)", text)
  for word in words:
    # if it's just white space, carry it through
    if re.match("\s", word):
      encoded_words.append(word)
    # else do a lot of stuff
    else:
      lowercase_word = word.lower()

      leading_punctuation = leadingPunctuation(lowercase_word)
      trailing_punctuation = trailingPunctuation(lowercase_word)
      stripped_word = stripWord(lowercase_word)
      
      encoded_word = encodeWord(stripped_word)
      
      encoded_word_with_punctuation = ""
      if leading_punctuation:
        encoded_word_with_punctuation += leading_punctuation
      if encoded_word:
        encoded_word_with_punctuation += encoded_word
      if trailing_punctuation:
        encoded_word_with_punctuation += trailing_punctuation
      encoded_word_with_punctuation += " " # add space after the word
      encoded_words.append(encoded_word_with_punctuation)
    
  # concatenate all the strings. this is a hacky StringBuilder
  return "".join(encoded_words)

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

def encodeWord(word):
  if len(word) is 0 or len(word) is 1:
    return word
  return word[0] + str(len(word)-2) + word[-1]

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print "Expected a single book title!"
    quit(1)

  title = sys.argv[1]
  title_file_name = "original_texts/{}.full.txt".format(title)
  full_text = read_file(title_file_name)
  encoded = encode(full_text)
  with open("output_texts/{}.encoded.txt".format(title), 'w') as output_file:
    output_file.write(encoded)
  # TODO: 