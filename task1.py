import random
# TASK 1: Hangman Game — CodeAlpha Internship

WORDS = ["python", "coding", "hangman", "laptop", "program"]

HANGMAN_STAGES = [
    """
       -----
       |   |
           |
           |
           |
           |
    =========""",
    """
       -----
       |   |
       O   |
           |
           |
           |
    =========""",
    """
       -----
       |   |
       O   |
       |   |
           |
           |
    =========""",
    """
       -----
       |   |
       O   |
      /|   |
           |
           |
    =========""",
    """
       -----
       |   |
       O   |
      /|\\  |
           |
           |
    =========""",
    """
       -----
       |   |
       O   |
      /|\\  |
      /    |
           |
    =========""",
    """
       -----
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    ========="""
]

def display_word(word, guessed_letters):
    """Show the word with guessed letters revealed."""
    return " ".join(letter if letter in guessed_letters else "_" for letter in word)

def hangman():
    print("\n" + "=" * 45)
    print("       🎮  HANGMAN GAME — CodeAlpha  🎮")
    print("=" * 45)

    word = random.choice(WORDS)
    guessed_letters = set()
    wrong_guesses = 0
    max_wrong = 6

    print(f"\n📝 The word has {len(word)} letters. You have {max_wrong} chances.\n")

    while wrong_guesses < max_wrong:
        print(HANGMAN_STAGES[wrong_guesses])
        print(f"\n🔤 Word: {display_word(word, guessed_letters)}")
        print(f"❌ Wrong guesses ({wrong_guesses}/{max_wrong}): {', '.join(sorted(guessed_letters - set(word))) or 'None'}")

        # Check win condition
        if all(letter in guessed_letters for letter in word):
            print(f"\n🎉 YOU WIN! The word was: '{word.upper()}' — Great job!\n")
            break

        guess = input("\n👉 Enter a letter: ").strip().lower()

        if len(guess) != 1 or not guess.isalpha():
            print("⚠️  Please enter a single letter only.")
            continue

        if guess in guessed_letters:
            print(f"⚠️  You already guessed '{guess}'. Try another letter.")
            continue

        guessed_letters.add(guess)

        if guess in word:
            print(f"✅ Nice! '{guess}' is in the word!")
        else:
            wrong_guesses += 1
            print(f"❌ Wrong! '{guess}' is not in the word.")

    else:
        print(HANGMAN_STAGES[max_wrong])
        print(f"\n💀 GAME OVER! The word was: '{word.upper()}'. Better luck next time!\n")

    play_again = input("🔄 Play again? (yes/no): ").strip().lower()
    if play_again in ("yes", "y"):
        hangman()
    else:
        print("\n👋 Thanks for playing! Goodbye!\n")

if __name__ == "__main__":
    hangman()