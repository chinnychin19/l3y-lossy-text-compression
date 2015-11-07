## L3y (Lossy compression)

Goal: Can we make a compressed novel that is barely human readable, but readable by a computer for > 90% of the words?
Example: a16z is andreessenhorowitz.

## Lossy Algorithm and Example

Step 1: Strip out all non-word characters. Word characters exist in [A-Z], [a-z], and [0-9].
Step 2: Convert all alphabet characters to lowercase.
Step 3: Replace each word with it's encoded form. (Words are space separated strings.)

Original text: "Hello, I am a robot!"
Compressed text: "h3o i a0m a r3t"

## Contributors

Tyler Nisonoff
Chinmay Patwardhan

## License

We are licensed to operate motor vehicles in the state of California. Other than that, I have no motivation to include anything valuable in this section.