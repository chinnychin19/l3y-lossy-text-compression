## L3y (Lossy compression)

Goal: Can we make a compressed novel that is barely human readable, but readable by a computer for > 90% of the words?

Example: a16z is andreessenhorowitz.

## Encoding (with example)

Desired function: `encode(String text) --> String`, where `text` is a large string of text (perhaps a novel)
- Step 1: Strip out all non-word characters. Word characters exist in [A-Z], [a-z], and [0-9].
- Step 2: Convert all alphabet characters to lowercase.
- Step 3: Replace each word with it's encoded form. (Words are space separated strings.)
    - if word is >= 3 characters of form a...z with D characters between the first and last character: aDz
    - if word is one character: just the character
    - if word is two characters of form "ab": a0b
- Step 4 (optional): remove spaces

Example:
- Original text: "Hello, I am a robot!"
- Compressed text: "h3o i a0m a r3t"
- Compressed without spaces: "h3o i a0m a r3t"

## Decoding (with example)

Desired function: `decode(String lossy_text) --> String`, where `lossy_text` is output from our `decode()` function. This should ideally output the original text for > 90% of the words.
- Step 1: Identify the boundaries of words in the input string. This is really easy if we included spaces in the encoded string. Fortunately, a single regular expression can accurately capture all of the words in the input string whether or not they are space separated: `/\w(?:\d\w)?/g` (You can play with regular expressions at https://regex101.com/.)
- Step 2: Replace the word with our guess of the original word
    - If the word is one or two characters (i.e. the encoded word is of the form "a" or "a0b"), this is deterministic.
    - Otherwise, this requires some stats. We can make our best guess at the original word by basing guesses on a set of training texts.

Example:
- lossy_text: "h3o i a0m a r3t"
- decoded guess option 1: "hello i am a robot" (100% correct)
- decoded guess option 2: "hello i am a reset" (80% correct)

## Open question

What the hell are we gonna do about punctuation, new lines, etc?

## Contributors

Tyler Nisonoff and Chinmay Patwardhan

## License

We are licensed to operate motor vehicles in the state of California. Other than that, we have no motivation to include anything valuable in this section.