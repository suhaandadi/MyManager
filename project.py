import sys
import csv
import os
import validators
import tabulate
import re
from pyfiglet import Figlet

figlet = Figlet()
#VALIDATION TESTS
def validate_email(email):
    if validators.email(email):
        return True
    else:
        return False

def validate_phone_number(number):
    if re.match(r"^\d{10}$", number):
        return True
    else:
        return False

def validate_date(date):
    if re.match(r"^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-(\d{4})$", date):
        return True
    else:
        return False

#Main menu
def main():
    print(figlet.renderText("MyManager"))
    while True:
        print("What do you want to do?")
        print("1. Add client")
        print("2. Search client")
        print("3. Add reminder")
        print("4. Load reminders")
        print("5. Exit")
        print("enter 1,2,3,4 or 5 based on your requirement.")
        choice = input("Enter your choice: ")
        if choice == "1":
            addclients()
        elif choice == "2":
            clientsearch()
        elif choice == "3":
            addreminder()
        elif choice == "4":
            load_reminders()
        elif choice == "5":
            print(figlet.renderText("Goodbye!"))
            break
        else:
            print("Invalid choice. Please enter 1,2,3,4 or 5")

#Features
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(SCRIPT_DIR, "clients.csv")
def addclients():
    clients = {}
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 3:
                    name, email, number = row
                    clients[name] = {"email": email, "number": number}


    name = input("Name: ").strip().lower()
    if name in clients:
        print("Client already exists.")
        sys.exit(1)


    email = input("Email: ")
    if not validate_email(email):
        print("Enter a valid email address.")
        sys.exit(1)
    if email in [info["email"] for info in clients.values()]:
        print("Email already exists.")
        sys.exit(1)


    try:
        number = input("Number: ").strip()

        if not validate_phone_number(number):
            print("Enter a valid 10-digit phone number.")
            sys.exit(1)
    except ValueError:
        print("Only numbers are allowed.")
        sys.exit(1)

    if number in [info["number"] for info in clients.values()]:
        print("Number already exists.")
        sys.exit(1)


    clients[name] = {"email": email, "number": number}
    table_data = []
    for name, info in clients.items():
        table_data.append([name, info["email"], info["number"]])

    with open("clients.csv", "a") as f:
        f.write(f"{name},{email},{number}\n")
    print(figlet.renderText("SUCCESS"))
    print("Client added successfully!\n")


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(SCRIPT_DIR, "clients.csv")
def clientsearch():
    info = input("Search: ").strip().lower()
    clients = []
    with open("clients.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 3:
                clients.append(row)
    for client in clients:
        if info in client:
            print(tabulate.tabulate([client], headers=["Name", "Email", "Phone"], tablefmt="rounded_outline"))
            break

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(SCRIPT_DIR, "reminders.csv")
def addreminder():
    reminder = {}
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 4:
                    name, date, note, priority = row
                    reminder[name] = {"date": date, "note": note, "priority": priority}


    name = input("Name: ").strip().lower()


    date = input("Date(DD-MM-YYYY): ")
    if not validate_date(date):
        print("Enter a valid date in the format DD-MM-YYYY.")
        sys.exit(1)


    note = input("Note: ")
    if len(note) > 50:
        print("Note must be less than 50 characters.")
        sys.exit(1)


    priority = int(input("Priority (1-3): "))
    try:
        priority = int(priority)
        if not (1 <= priority <= 3):
            raise ValueError
    except ValueError:
        print("Priority must be an integer between 1(Highest) and 3(Lowest).")
        sys.exit(1)


    reminder[name] = {"date": date, "note": note, "priority": priority}
    with open("reminders.csv", "a") as f:
        f.write(f"{priority},{name},{date},{note}\n")
    print(figlet.renderText("SUCCESS"))
    print("Reminder added successfully!\n")


def load_reminders():
    reminders = []
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 4:
                    priority, name, date, note = row
                    reminders.append({"priority": priority, "name": name, "date": date, "note": note})
            for reminder in sorted(reminders, key=lambda x: x["priority"]):
                print(tabulate.tabulate([[reminder["name"], reminder["date"], reminder["note"]]], headers=["Name", "Date", "Note"], tablefmt="rounded_outline"))

if __name__ == "__main__":
    main()
