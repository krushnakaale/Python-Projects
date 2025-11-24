# Number Guessing Game - Beginner Project 2

import random


def guessing_game():
    print("=" * 50)
    print("Number Guessing Game")
    print("=" * 50)
    print("I have selected a number between 1 and 100.")
    print("Try to guess it!\n")

    # Generate a random number
    secret_number = random.randint(1, 100)
    attempts = 0
    max_attempts = 10

    while attempts < max_attempts:
        try:
            guess = int(input(f"Attempt {attempts + 1}/{max_attempts} - Your guess: "))
            attempts += 1

            if guess < 1 or guess > 100:
                print("Please enter a number between 1 and 100.")
                continue

            if guess < secret_number:
                print("Try a higher number.")
            elif guess > secret_number:
                print("Try a lower number.")
            else:
                print("\nCongratulations! You guessed the correct number.")
                print(f"Correct number: {secret_number}")
                print(f"You won in {attempts} attempts.")

                # Calculate score
                score = (max_attempts - attempts + 1) * 10
                print(f"Your score: {score} points\n")
                break

        except ValueError:
            print("Please enter a valid number.")

    else:
        print("\nGame Over! You lost.")
        print(f"The correct number was: {secret_number}\n")

    # Play again?
    play_again = input("Do you want to play again? (yes/no): ")
    if play_again.lower() in ["yes", "y"]:
        guessing_game()
    else:
        print("Thank you for playing!")


# Run the program
if __name__ == "__main__":
    guessing_game()
