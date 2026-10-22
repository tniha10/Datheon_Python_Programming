import random

words = ["apple", "lion", "chair", "neptune", "internship", "python", "hangman", "programming", "computer", "keyboard"]

secret_word = random.choice(words) # Choosing a random word from the list of words
word_length = len(secret_word) # Getting the length of the secret word
hidden_letter = ["_"] * word_length  # Creating a list of underscores to represent the hidden letters of the secret word
attempts_left = 6  # Setting the number of attempts left for the player

guessed_letters = set()  # Creating a set to keep track of the letters guessed by the player

while attempts_left > 0 and "_" in hidden_letter:  # Looping until the player runs out of attempts or guesses all letters
    print(" ".join(hidden_letter)) #join is used to concatenate the elements of the list into a single string, with spaces in between each element.
    guess = input("Guess a letter: ").lower()  # Prompting the user to guess a letter and converting it to lowercase for consistency

    if guess in guessed_letters:  # Checking if the letter has already been guessed
        print("You already guessed that letter. Try again.")
        continue  # Skipping the rest of the loop and prompting the user to guess again
    
    guessed_letters.add(guess.lower())  # Adding the guessed letter to the set of guessed letters

    # Checking if the guessed letter matches the letter in the secret word at the current index
    for index in range(word_length):
       if secret_word[index] == guess.lower():  
         hidden_letter[index] = secret_word[index] # Updating the hidden_letter list to reveal the correctly guessed letter at the corresponding index

    # print(type(hidden_letter)) -> checks the class 
    # hidden_letter[1] = "p" -> first this was wrong because strings are immutable in Python. You cannot change a character in a string directly.

    # Checking if the guessed letter is in the secret word
    if guess.lower() in secret_word:
       print("Correct guess!")
    else:
       print("Incorrect guess.")
       attempts_left -= 1  # Decreasing the number of attempts left
       print(f"Attempts left: {attempts_left}")

    print()  # Printing a blank line for better readability

if "_" not in hidden_letter:  # Checking if the player has guessed all letters
    print(f"Congratulations! You guessed the word: {secret_word}")
else:
    print(f"Game over! The secret word was: {secret_word}")  # Displaying the secret word when the player runs out of attempts