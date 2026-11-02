import random
from pathlib import Path

# Hangman drawings for 0 to 6 incorrect guesses
HANGMAN_STAGES = [
    """
       +---+
       |   |
           |
           |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
           |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
       |   |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|   |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
      /    |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    =========
    """
]


def load_words():
    # Read the word list from the same folder as this Python file
    file_path = Path(__file__).resolve().parent / "google-10000-english-no-swears.txt"

    with open(file_path, "r", encoding="utf-8") as file:
        words = [
            line.strip().lower()
            for line in file
            if line.strip().isalpha()
        ]

    return words


def choose_difficulty():
    print("\nChoose your difficulty:")
    print("1. Easy   (3-5 letters)")
    print("2. Medium (6-8 letters)")
    print("3. Hard   (9+ letters)")

    while True:
        choice = input("\nEnter 1, 2, or 3: ").strip()

        if choice in ["1", "2", "3"]:
            return choice

        print("Invalid choice. Please enter 1, 2, or 3.")


def choose_word(words, difficulty):
    if difficulty == "1":
        filtered_words = [word for word in words if 3 <= len(word) <= 5]

    elif difficulty == "2":
        filtered_words = [word for word in words if 6 <= len(word) <= 8]

    else:
        filtered_words = [word for word in words if len(word) >= 9]

    if not filtered_words:
        raise ValueError("No words found for this difficulty.")

    return random.choice(filtered_words)


def display_game(hidden_letter, guessed_letters, attempts_left):
    mistakes = 6 - attempts_left

    print("\n" + "=" * 40)
    print("            HANGMAN")
    print("=" * 40)

    print(HANGMAN_STAGES[mistakes])
    print("Word:", " ".join(hidden_letter))
    print(f"\nAttempts left: {attempts_left}/6")

    if guessed_letters:
        print("Guessed letters:", ", ".join(sorted(guessed_letters)))
    else:
        print("Guessed letters: None")

    print("=" * 40)


def play_game(words):
    difficulty = choose_difficulty()
    secret_word = choose_word(words, difficulty)

    word_length = len(secret_word)
    hidden_letter = ["_"] * word_length
    attempts_left = 6
    guessed_letters = set()

    print("\nA secret word has been selected!")
    print(f"The word contains {word_length} letters.")
    print("You have 6 chances. Good luck!")

    while attempts_left > 0 and "_" in hidden_letter:
        display_game(hidden_letter, guessed_letters, attempts_left)

        guess = input("\nGuess a letter: ").strip().lower()

        # Only accept a single English letter
        if len(guess) != 1 or guess not in "abcdefghijklmnopqrstuvwxyz":
            print("\nPlease enter only one English letter.")
            continue

        if guess in guessed_letters:
            print("\nYou already guessed that letter. Try another!")
            continue

        guessed_letters.add(guess)

        if guess in secret_word:
            # Reveal every position containing the correct letter
            for index in range(word_length):
                if secret_word[index] == guess:
                    hidden_letter[index] = guess

            print("\nCorrect guess! Well done!")

        else:
            attempts_left -= 1
            print("\nOops! That letter is not in the word.")

            if attempts_left == 2:
                print(f"Hint: The word starts with '{secret_word[0]}'.")

    display_game(hidden_letter, guessed_letters, attempts_left)

    if "_" not in hidden_letter:
        print("\n" + "*" * 40)
        print("          YOU WIN!")
        print("*" * 40)
        print(f"Congratulations! The word was: {secret_word}")
        print(f"Remaining attempts: {attempts_left}")

    else:
        print("\n" + "*" * 40)
        print("          GAME OVER!")
        print("*" * 40)
        print(f"The secret word was: {secret_word}")
        print("Better luck next time!")


def main():
    print("=" * 45)
    print("       WELCOME TO HANGMAN!")
    print("=" * 45)
    print("Guess the hidden word before the drawing")
    print("of the hangman is completed!")

    try:
        words = load_words()

        if not words:
            print("The word list is empty!")
            return

    except FileNotFoundError:
        print("Error: Word list file not found.")
        print("Make sure the TXT file is in the same folder.")
        return

    while True:
        play_game(words)

        replay = input("\nWould you like to play again? (yes/no): ").strip().lower()

        if replay not in ["yes", "y"]:
            print("\nThanks for playing Hangman!")
            print("See you next time!")
            break


if __name__ == "__main__":
    main()
