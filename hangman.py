#A tool for choosing a random word
import random

# List of possible secret words
words = ["apple", "lion", "chair", "neptune", "internship", "python", "hangman", "programming", "computer", "keyboard"]

# Choosing a random word from the list
secret_word = random.choice(words)
# Getting the length of the secret word
word_length = len(secret_word)

hidden_word = "_" * word_length  # Creating a hidden representation of the secret word

# Displaying the secret word and its length to the console (for testing purposes)
print(secret_word)
print(word_length)
print(hidden_word)