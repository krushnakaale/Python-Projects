# Rock Paper Scissors - Beginner Project 3

import random


def rock_paper_scissors():
    print("Rock Paper Scissors Game")
    print("-" * 50)

    choices = ["rock", "paper", "scissors"]

    player_score = 0
    computer_score = 0
    rounds = 0

    print("\nInstructions:")
    print("- Rock beats scissors")
    print("- Scissors beats paper")
    print("- Paper beats rock")
    print("\nBest of 5 rounds!\n")

    while rounds < 5:
        print(f"\n--- Round {rounds + 1} ---")
        print("Choose: rock, paper, scissors (or type 'quit' to exit)")

        player_choice = input("Your choice: ").lower()

        if player_choice == "quit":
            print("Game ended.")
            break

        if player_choice not in choices:
            print("Invalid choice! Please select 'rock', 'paper', or 'scissors'.")
            continue

        computer_choice = random.choice(choices)
        rounds += 1

        print(f"\nYou chose: {player_choice}")
        print(f"Computer chose: {computer_choice}")

        # Decide winner
        if player_choice == computer_choice:
            print("Result: Draw")
        elif (
            (player_choice == "rock" and computer_choice == "scissors")
            or (player_choice == "paper" and computer_choice == "rock")
            or (player_choice == "scissors" and computer_choice == "paper")
        ):
            print("Result: You win this round")
            player_score += 1
        else:
            print("Result: Computer wins this round")
            computer_score += 1

        print(f"\nScore - You: {player_score} | Computer: {computer_score}")

    # Final result
    if rounds == 5:
        print("\n" + "=" * 50)
        print("FINAL RESULT")
        print("=" * 50)
        print(f"Your score: {player_score}")
        print(f"Computer's score: {computer_score}")

        if player_score > computer_score:
            print("\nCongratulations! You won the game.")
        elif player_score < computer_score:
            print("\nComputer won the game. Better luck next time.")
        else:
            print("\nThe game ended in a draw.")

    # Play again?
    play_again = input("\nDo you want to play again? (yes/no): ")
    if play_again.lower() in ["yes", "y"]:
        rock_paper_scissors()
    else:
        print("Thank you for playing!")


# Run the program
if __name__ == "__main__":
    rock_paper_scissors()
