"""
Professional Expense Tracker

A command-line expense tracking application that allows users to:
- Add expenses
- View all expenses
- Search expenses by category
- View spending summaries
- Delete expenses

Expense data is stored locally in a JSON file so that it persists
between program executions.
"""

import json
from datetime import datetime
from pathlib import Path


# File used to permanently store expense data.
DATA_FILE = Path("expenses.json")

# Currency symbol used by the application.
CURRENCY_SYMBOL = "₹"


def load_expenses() -> list:
    """
    Load expenses from the JSON data file.

    Returns:
        A list containing all saved expenses.
        Returns an empty list if the file does not exist or
        contains invalid JSON.
    """

    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        print("Warning: Unable to read expense data.")
        return []


def save_expenses(expenses: list) -> None:
    """
    Save expenses to the JSON data file.

    Args:
        expenses: List of expense dictionaries to save.
    """

    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(expenses, file, indent=4)

    except OSError:
        print("Error: Unable to save expense data.")


def get_positive_amount() -> float:
    """
    Ask the user for a valid positive expense amount.

    Returns:
        A positive floating-point number.
    """

    while True:
        try:
            amount = float(input("Enter amount: ₹"))

            if amount <= 0:
                print("Amount must be greater than zero.")
                continue

            return amount

        except ValueError:
            print("Please enter a valid amount.")


def add_expense(expenses: list) -> None:
    """
    Add a new expense to the expense list.

    Args:
        expenses: Current list of expenses.
    """

    print("\n" + "=" * 45)
    print("                ADD EXPENSE")
    print("=" * 45)

    amount = get_positive_amount()

    category = input("Enter category: ").strip()

    while not category:
        print("Category cannot be empty.")
        category = input("Enter category: ").strip()

    description = input("Enter description: ").strip()

    while not description:
        print("Description cannot be empty.")
        description = input("Enter description: ").strip()

    # Generate a unique ID using the current timestamp.
    expense_id = (
        datetime.now().strftime("%Y%m%d%H%M%S%f")
    )

    # Store the current date and time.
    date = datetime.now().strftime("%d-%m-%Y %H:%M")

    expense = {
        "id": expense_id,
        "amount": amount,
        "category": category.title(),
        "description": description,
        "date": date,
    }

    expenses.append(expense)
    save_expenses(expenses)

    print("\nExpense added successfully!")
    print(f"Amount: {CURRENCY_SYMBOL}{amount:.2f}")
    print(f"Category: {category.title()}")
    print(f"Description: {description}")


def view_expenses(expenses: list) -> None:
    """
    Display all recorded expenses.

    Args:
        expenses: List of expenses.
    """

    print("\n" + "=" * 75)
    print("                         ALL EXPENSES")
    print("=" * 75)

    if not expenses:
        print("No expenses recorded yet.")
        return

    print(
        f"{'ID':<6}"
        f"{'Date':<20}"
        f"{'Category':<15}"
        f"{'Amount':<12}"
        f"Description"
    )

    print("-" * 75)

    for index, expense in enumerate(expenses, start=1):
        print(
            f"{index:<6}"
            f"{expense['date']:<20}"
            f"{expense['category']:<15}"
            f"{CURRENCY_SYMBOL}{expense['amount']:<11.2f}"
            f"{expense['description']}"
        )

    print("-" * 75)

    total = sum(expense["amount"] for expense in expenses)

    print(f"{'Total Spending:':<41}"
          f"{CURRENCY_SYMBOL}{total:.2f}")


def search_by_category(expenses: list) -> None:
    """
    Search and display expenses belonging to a category.

    Args:
        expenses: List of expenses.
    """

    print("\n" + "=" * 45)
    print("             SEARCH EXPENSES")
    print("=" * 45)

    if not expenses:
        print("No expenses available.")
        return

    category = input("Enter category to search: ").strip().lower()

    results = [
        expense
        for expense in expenses
        if expense["category"].lower() == category
    ]

    if not results:
        print(f"No expenses found for '{category}'.")
        return

    print(f"\nExpenses in category: {category.title()}")
    print("-" * 60)

    category_total = 0

    for expense in results:
        print(
            f"{expense['date']} | "
            f"{expense['description']} | "
            f"{CURRENCY_SYMBOL}{expense['amount']:.2f}"
        )

        category_total += expense["amount"]

    print("-" * 60)
    print(
        f"Category Total: "
        f"{CURRENCY_SYMBOL}{category_total:.2f}"
    )


def spending_summary(expenses: list) -> None:
    """
    Display a summary of total spending by category.

    Args:
        expenses: List of expenses.
    """

    print("\n" + "=" * 45)
    print("             SPENDING SUMMARY")
    print("=" * 45)

    if not expenses:
        print("No expenses recorded yet.")
        return

    category_totals = {}

    for expense in expenses:
        category = expense["category"]
        amount = expense["amount"]

        category_totals[category] = (
            category_totals.get(category, 0) + amount
        )

    total = sum(category_totals.values())

    for category, amount in sorted(
        category_totals.items(),
        key=lambda item: item[1],
        reverse=True,
    ):
        percentage = (amount / total) * 100

        print(
            f"{category:<20}"
            f"{CURRENCY_SYMBOL}{amount:>10.2f}"
            f"  ({percentage:.1f}%)"
        )

    print("-" * 45)
    print(f"{'Total Spending:':<20}"
          f"{CURRENCY_SYMBOL}{total:.2f}")


def delete_expense(expenses: list) -> None:
    """
    Delete an expense selected by its displayed number.

    Args:
        expenses: List of expenses.
    """

    print("\n" + "=" * 45)
    print("             DELETE EXPENSE")
    print("=" * 45)

    if not expenses:
        print("No expenses available to delete.")
        return

    view_expenses(expenses)

    while True:
        try:
            choice = int(
                input("\nEnter expense number to delete: ")
            )

            if not 1 <= choice <= len(expenses):
                print("Please enter a valid expense number.")
                continue

            deleted_expense = expenses.pop(choice - 1)
            save_expenses(expenses)

            print("\nExpense deleted successfully!")
            print(
                f"Deleted: "
                f"{deleted_expense['description']} - "
                f"{CURRENCY_SYMBOL}"
                f"{deleted_expense['amount']:.2f}"
            )

            break

        except ValueError:
            print("Please enter a valid number.")


def display_menu() -> None:
    """Display the main application menu."""

    print("\n" + "=" * 45)
    print("             EXPENSE TRACKER")
    print("=" * 45)

    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Search by Category")
    print("4. Spending Summary")
    print("5. Delete Expense")
    print("6. Exit")

    print("=" * 45)


def main() -> None:
    """Run the Expense Tracker application."""

    expenses = load_expenses()

    print("\nWelcome to the Expense Tracker!")

    while True:
        display_menu()

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_expense(expenses)

        elif choice == "2":
            view_expenses(expenses)

        elif choice == "3":
            search_by_category(expenses)

        elif choice == "4":
            spending_summary(expenses)

        elif choice == "5":
            delete_expense(expenses)

        elif choice == "6":
            print("\nThank you for using Expense Tracker!")
            print("Goodbye!")
            break

        else:
            print("\nInvalid choice. Please select 1-6.")


# Run the application only when this file is executed directly.
if __name__ == "__main__":
    main()