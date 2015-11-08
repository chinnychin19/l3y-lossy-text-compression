## L3y (Lossy compression)

Goal: Can we make a compressed novel that is barely human readable, but readable by a computer for > 90% of the words?

Example: a16z is andreessenhorowitz.

## Encoding (with example)

Desired function: `encode(String text) --> String`, where `text` is a large string of text (perhaps a novel)

`This section needs to be updated`

Example:
- Original text: "Hello, I am a robot!"
- Compressed text: "h3o i a0m a r3t"

## Decoding (with example)

Desired function: `decode(String lossy_text) --> String`, where `lossy_text` is output from our `decode()` function. This should ideally output the original text for > 90% of the words.
- Step 1: Identify the boundaries of words in the input string. This is really easy if we included spaces in the encoded string. Fortunately, a single regular expression can accurately capture all of the words in the input string: `/([^\w\s]*\w(?:\d+\w)?[^\w\s]*)|(\S+|[\n\r\t\f]+)/g` (You can play with regular expressions at https://regex101.com/.)
- Step 2: Replace the word with our guess of the original word
    - Ignore punctuation when decoding because we aren't making any changes to the original punctuation while encoding
    - If the word is one or two characters (i.e. the encoded word is of the form "a" or "a0b"), this is deterministic.
    - Otherwise, this requires some stats. We can make our best guess at the original word by basing guesses on a set of training texts.

Example:
- lossy_text: "h3o i a0m a r3t"
- decoded guess option 1: "hello i am a robot" (100% correct)
- decoded guess option 2: "hello i am a reset" (80% correct)

## Open questions

No questions at the moment... There will certainly be some soon.

## Contributors

Tyler Nisonoff and Chinmay Patwardhan

## License

We are licensed to operate motor vehicles in the state of California. Other than that, we have no motivation to include anything valuable in this section.