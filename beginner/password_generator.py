# Password Generator - Beginner Project 4

import random
import string


def generate_password(length, use_uppercase, use_numbers, use_symbols):
    """
    Generate a password based on user preferences.
    """
    characters = string.ascii_lowercase  # a-z

    if use_uppercase:
        characters += string.ascii_uppercase  # A-Z
    if use_numbers:
        characters += string.digits  # 0-9
    if use_symbols:
        characters += string.punctuation  # !@#$%^&*

    # Generate random password
    password = "".join(random.choice(characters) for _ in range(length))
    return password


def password_strength(password):
    """
    Check how strong the password is.
    """
    strength = 0

    if len(password) >= 8:
        strength += 1
    if any(c.isupper() for c in password):
        strength += 1
    if any(c.isdigit() for c in password):
        strength += 1
    if any(c in string.punctuation for c in password):
        strength += 1

    if strength == 4:
        return "Very Strong"
    elif strength == 3:
        return "Strong"
    elif strength == 2:
        return "Medium"
    else:
        return "Weak"


def password_generator():
    print("Password Generator")
    print("-" * 60)

    while True:
        print("\n--- Password Settings ---")

        # Take length
        try:
            length = int(input("Password length (6-50): "))
            if length < 6 or length > 50:
                print("Length must be between 6 and 50.")
                continue
        except ValueError:
            print("Please enter a valid number.")
            continue

        # Options
        print("\nInclude:")
        use_uppercase = input("Uppercase letters (A-Z)? (yes/no): ").lower() in [
            "yes",
            "y",
        ]
        use_numbers = input("Numbers (0-9)? (yes/no): ").lower() in ["yes", "y"]
        use_symbols = input("Symbols (!@#$%^&*)? (yes/no): ").lower() in ["yes", "y"]

        # Generate password
        password = generate_password(length, use_uppercase, use_numbers, use_symbols)
        strength = password_strength(password)

        # Display result
        print("Generated Password:")
        print("-" * 60)
        print(f"Password: {password}")
        print(f"Length: {len(password)} characters")
        print(f"Strength: {strength}")
        print("-" * 60)

        # Options
        print("\nOptions:")
        print("1. Generate another password")
        print("2. Change settings")
        print("3. Exit")

        choice = input("\nYour choice (1-3): ")

        if choice == "1":
            # Generate new password with same settings
            password = generate_password(
                length, use_uppercase, use_numbers, use_symbols
            )
            strength = password_strength(password)
            print(f"\nNew Password: {password}")
            print(f"Strength: {strength}")
        elif choice == "2":
            continue
        elif choice == "3":
            print("\nThank you!")
            print("Please keep your passwords safe.")
            break
        else:
            print("Invalid choice!")


# Run the program
if __name__ == "__main__":
    password_generator()
