def add(x, y):
    return x + y


def subtract(x, y):
    return x - y


def multiply(x, y):
    return x * y


def divide(x, y):
    if y == 0:
        return "Error! Cannot divide by zero."
    return x / y


def calculator():
    print("Simple Calculator")
    print("-" * 40)

    while True:
        print("\nOperations:")
        print("1. Add (+)")
        print("2. Subtract (-)")
        print("3. Multiply (*)")
        print("4. Divide (/)")
        print("5. Exit")

        choice = input("\nEnter your choice (1–5): ")

        if choice == "5":
            print("Quitting program...")
            break

        if choice in ["1", "2", "3", "4"]:
            try:
                num1 = float(input("Enter the first number: "))
                num2 = float(input("Enter the second number: "))

                if choice == "1":
                    print(f"\nResult: {num1} + {num2} = {add(num1, num2)}")
                elif choice == "2":
                    print(f"\nResult: {num1} - {num2} = {subtract(num1, num2)}")
                elif choice == "3":
                    print(f"\nResult: {num1} * {num2} = {multiply(num1, num2)}")
                elif choice == "4":
                    print(f"\nResult: {num1} / {num2} = {divide(num1, num2)}")

                # --- Ask user to continue ---
                again = input(
                    "\nDo you want to perform another operation? (y/n): "
                ).lower()
                if again != "y":
                    print("Quitting program...")
                    break

            except ValueError:
                print("Error: Please enter a valid number.")
        else:
            print("Invalid choice! Please choose an option between 1 - 5.")


if __name__ == "__main__":
    calculator()
