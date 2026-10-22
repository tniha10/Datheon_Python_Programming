#A tool for choosing a random word
import random

# List of possible secret words
words = ["apple", "lion", "chair", "neptune", "internship", "python", "hangman", "programming", "computer", "keyboard"]

# Choosing a random word from the list
secret_word = random.choice(words)

# Displaying the secret word to the console (for testing purposes)
print(secret_word)