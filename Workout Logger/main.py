import gspread
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from colorama import Fore, Style, init
from datetime import datetime

# Initialize colorama
init(autoreset=True)

# --- Google Sheets Setup --- #
SCOPE = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("Workout Log")
worksheet = SHEET.worksheet("logs")

# --- Safety Questions --- #
def run_safety_check():
    print(Fore.CYAN + "\n=== Safety Check Before Workout ===")
    questions = [
        "Do you have a heart condition?",
        "Do you feel pain in your chest during physical activity?",
        "Are you currently pregnant?",
        "Do you have any joint or bone problems?",
        "Do you experience dizziness or loss of balance?"
    ]
    for question in questions:
        while True:
            answer = input(f"{question} (Yes/No): ").strip().lower()
            if answer == "yes":
                print(Fore.GREEN + "Thank you for your answer.")
                break
            elif answer == "no":
                print(Fore.GREEN + "Thank you for your answer.")
                break
            else:
                print(Fore.RED + "Invalid input. Please answer Yes or No.")

# --- Add a Workout Entry --- #
def add_workout():
    print(Fore.CYAN + "\n=== Log Your Workout ===")
    exercise = input("What exercise did you do? ").strip().title()
    while True:
        try:
            duration = int(input("How many minutes did you exercise? ").strip())
            break
        except ValueError:
            print(Fore.RED + "Please enter a valid number of minutes.")

    while True:
        intensity = input("What was the intensity? (Low / Medium / High): ").strip().capitalize()
        if intensity in ["Low", "Medium", "High"]:
            break
        else:
            print(Fore.RED + "Please enter Low, Medium, or High.")

    date = datetime.now().strftime("%d/%m/%Y")
    worksheet.append_row([date, exercise, duration, intensity])
    print(Fore.GREEN + "Workout logged successfully!\n")

# --- View Logged Workouts --- #
def view_workouts():
    print(Fore.CYAN + "\n=== Your Logged Workouts ===")
    records = worksheet.get_all_values()
    for row in records[1:]:  # Skip header
        print(f"Date: {row[0]} | Exercise: {row[1]} | Duration: {row[2]} mins | Intensity: {row[3]}")

# --- Main Menu --- #
def main():
    print(Fore.YELLOW + "Welcome to Workout Logger! 💪")
    run_safety_check()

    while True:
        print("\nWhat would you like to do?")
        print("1. Add a new workout")
        print("2. View all logged workouts")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == "1":
            add_workout()
        elif choice == "2":
            view_workouts()
        elif choice == "3":
            print(Fore.MAGENTA + "Goodbye! Stay strong! 💙")
            break
        else:
            print(Fore.RED + "Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()
