
from datetime import datetime, timedelta

# ==========================================
# STUDENT EXPENSE TRACKER
# ==========================================

allowance = 0.0
expenses = []

CATEGORIES = {
    "1": "Food",
    "2": "Transportation",
    "3": "School Supplies",
    "4": "Load/Internet",
    "5": "Other"
}


# ---------- HELPER FUNCTIONS ----------

def get_total_expenses():
    return sum(
        e["amount"] for e in expenses if not e["voided"]
    )


def get_remaining_balance():
    return allowance - get_total_expenses()


def get_amount(prompt):
    try:
        amount = float(input(prompt))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return None

        return amount

    except ValueError:
        print("Please enter a valid amount.")


def choose_category():
    print("\n========== CATEGORIES ==========")

    for number, category in CATEGORIES.items():
        print(f"{number}. {category}")

    choice = input("Choose category: ")
    return CATEGORIES.get(choice)


# ---------- ALLOWANCE ----------

def set_allowance():
    global allowance

    try:
        amount = float(input("Enter allowance amount: ₱"))

        if amount < 0:
            print("Allowance cannot be negative.")
            return

        if amount < get_total_expenses():
            print("INSUFFICIENT BALANCE!")
            print("Allowance cannot be less than your expenses.")
            return

        allowance = amount

        print(f"Allowance updated to ₱{allowance:.2f}")
        print(f"Remaining balance: ₱{get_remaining_balance():.2f}")

    except ValueError:
        print("Please enter a valid amount.")


# ---------- ADD EXPENSE ----------

def add_expense():
    amount = get_amount("Enter expense amount: ₱")

    if amount is None:
        return

    balance = get_remaining_balance()

    if amount > balance:
        print("\nINSUFFICIENT BALANCE!")
        print(f"Remaining balance: ₱{balance:.2f}")
        print("Expense rejected. You cannot exceed your budget.")
        return

    category = choose_category()

    if category is None:
        print("Invalid category.")
        return

    description = input("Enter description: ").strip()

    if not description:
        print("Description cannot be empty.")
        return

    expenses.append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "description": description,
        "category": category,
        "amount": amount,
        "voided": False
    })

    print("\nExpense recorded successfully!")
    print(f"Remaining balance: ₱{get_remaining_balance():.2f}")


# ---------- VIEW AND FILTER EXPENSES ----------

def view_expenses():
    if not expenses:
        print("\nNo expenses recorded.")
        return

    print("\n========== EXPENSE RECORDS ==========")

    for i, e in enumerate(expenses, start=1):
        status = "VOIDED" if e["voided"] else "ACTIVE"

        print(
            f"{i}. {e['date']} | {e['description']} | "
            f"{e['category']} | ₱{e['amount']:.2f} | {status}"
        )


def expense_records_menu():
    while True:
        print("\n========== EXPENSE RECORDS ==========")
        print("1. View All Expenses")
        print("2. Filter by Category")
        print("3. Back to Main Menu")

        choice = input("Choose an option: ")

        if choice == "1":
            view_expenses()

        elif choice == "2":
            category = choose_category()

            if category is None:
                print("Invalid category.")
                continue

            found = False
            total = 0

            print(f"\n========== {category.upper()} ==========")

            for i, e in enumerate(expenses, start=1):
                if e["category"] == category and not e["voided"]:
                    print(
                        f"{i}. {e['date']} | {e['description']} | "
                        f"₱{e['amount']:.2f}"
                    )
                    total += e["amount"]
                    found = True

            if found:
                print(f"Category Total: ₱{total:.2f}")
            else:
                print("No active expenses found.")

        elif choice == "3":
            break

        else:
            print("Invalid choice.")


# ---------- VOID EXPENSE ----------

def void_expense():
    view_expenses()

    if not any(not e["voided"] for e in expenses):
        print("No active expenses to void.")
        return

    try:
        number = int(input("\nEnter expense number to void: "))

        if number < 1 or number > len(expenses):
            print("Invalid expense number.")
            return

        expense = expenses[number - 1]

        if expense["voided"]:
            print("This expense is already voided.")
            return

        expense["voided"] = True

        print("Expense voided successfully.")
        print(f"Updated balance: ₱{get_remaining_balance():.2f}")

    except ValueError:
        print("Please enter a valid number.")


# ---------- EXPENSE REPORTS ----------

def expense_reports():
    while True:
        print("\n========== EXPENSE REPORTS ==========")
        print("1. Daily Expenses")
        print("2. Weekly Expenses")
        print("3. Monthly Expenses")
        print("4. Spending by Category")
        print("5. Back to Main Menu")

        choice = input("Choose a report: ")

        if choice == "5":
            break

        if choice == "4":
            spending_by_category()
            continue

        today = datetime.now().date()

        if choice == "1":
            start_date = today
            end_date = today
            title = "DAILY EXPENSES"

        elif choice == "2":
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)
            title = "WEEKLY EXPENSES"

        elif choice == "3":
            start_date = today.replace(day=1)

            if today.month == 12:
                next_month = today.replace(
                    year=today.year + 1, month=1, day=1
                )
            else:
                next_month = today.replace(
                    month=today.month + 1, day=1
                )

            end_date = next_month - timedelta(days=1)
            title = "MONTHLY EXPENSES"

        else:
            print("Invalid choice.")
            continue

        matching = []

        for e in expenses:
            expense_date = datetime.strptime(
                e["date"], "%Y-%m-%d"
            ).date()

            if (
                start_date <= expense_date <= end_date
                and not e["voided"]
            ):
                matching.append(e)

        print(f"\n========== {title} ==========")
        print(f"Period: {start_date} to {end_date}")

        total = 0

        for e in matching:
            print(
                f"{e['date']} | {e['description']} | "
                f"{e['category']} | ₱{e['amount']:.2f}"
            )
            total += e["amount"]

        if not matching:
            print("No expenses recorded for this period.")

        print(f"Number of Expenses: {len(matching)}")
        print(f"Total Expenses: ₱{total:.2f}")


def spending_by_category():
    print("\n====== SPENDING BY CATEGORY ======")

    for category in CATEGORIES.values():
        total = sum(
            e["amount"] for e in expenses
            if e["category"] == category and not e["voided"]
        )
        print(f"{category}: ₱{total:.2f}")


# ---------- BUDGET SUMMARY AND INSIGHTS ----------

def budget_summary_insights():
    total = get_total_expenses()
    remaining = get_remaining_balance()

    percentage = total / allowance * 100 if allowance > 0 else 0

    print("\n========== BUDGET SUMMARY ==========")
    print(f"Total Allowance:   ₱{allowance:.2f}")
    print(f"Total Expenses:    ₱{total:.2f}")
    print(f"Remaining Balance: ₱{remaining:.2f}")
    print(f"Spending:          {percentage:.2f}%")

    if allowance == 0:
        status = "NOT SET"
    elif remaining == 0:
        status = "CRITICAL"
    elif percentage >= 90:
        status = "CRITICAL"
    elif percentage >= 80:
        status = "WARNING"
    elif percentage >= 50:
        status = "MODERATE"
    else:
        status = "HEALTHY"

    print(f"Budget Status:     {status}")

    if allowance == 0:
        print("Please set your allowance first.")
    elif remaining == 0:
        print("WARNING: Your budget is fully used!")

    active = [e for e in expenses if not e["voided"]]

    print("\n========== BUDGET INSIGHTS ==========")

    if not active:
        print("No expense data available.")
        return

    dates = {e["date"] for e in active}
    average_daily = total / len(dates)

    print(f"Average Spending per Recorded Day: ₱{average_daily:.2f}")

    category_totals = {}

    for e in active:
        category = e["category"]
        category_totals[category] = (
            category_totals.get(category, 0) + e["amount"]
        )

    highest = max(category_totals, key=category_totals.get)

    print(
        f"Highest Spending Category: {highest} "
        f"(₱{category_totals[highest]:.2f})"
    )


# ---------- MAIN MENU ----------

def main():
    while True:
        print("\n" + "=" * 45)
        print("       STUDENT EXPENSE TRACKER")
        print("=" * 45)
        print("1. Set/Edit Allowance")
        print("2. Add Expense")
        print("3. View Expense Records")
        print("4. Expense Reports")
        print("5. Void Expense")
        print("6. Budget Summary & Insights")
        print("7. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            set_allowance()
        elif choice == "2":
            add_expense()
        elif choice == "3":
            expense_records_menu()
        elif choice == "4":
            expense_reports()
        elif choice == "5":
            void_expense()
        elif choice == "6":
            budget_summary_insights()
        elif choice == "7":
            print("Thank you for using Student Expense Tracker!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
