import random

words = ["apple", "lion", "chair", "neptune", "internship", "python", "hangman", "programming", "computer", "keyboard"]

secret_word = random.choice(words) # Choosing a random word from the list of words
word_length = len(secret_word) # Getting the length of the secret word
hidden_letter = ["_"] * word_length  # Creating a list of underscores to represent the hidden letters of the secret word

print(" ".join(hidden_letter)) #join is used to concatenate the elements of the list into a single string, with spaces in between each element.

guess = input("Guess a letter: ")  # Prompting the user to guess a letter

# Checking if the guessed letter matches the letter in the secret word at the current index
for index in range(word_length):
    if secret_word[index] == guess.lower():  
       hidden_letter[index] = secret_word[index] # Updating the hidden_letter list to reveal the correctly guessed letter at the corresponding index

# print(type(hidden_letter)) -> checks the class 
# hidden_letter[1] = "p" -> first this was wrong because strings are immutable in Python. You cannot change a character in a string directly.

print(" ".join(hidden_letter)) # Displaying the updated hidden letters after the guess

# Checking if the guessed letter is in the secret word
if guess.lower() in secret_word:
    print("Correct guess!")
else:
    print("Incorrect guess.")