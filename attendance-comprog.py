import datetime
import os

ACCOUNTS = {
    "admin": {
        "password": "admin123",
        "student_id": "Administrator"
    }
}

today = datetime.date.today().strftime("%b %d, %Y")
ATTENDANCE_FILE = f"Attendance Log ({today}).txt"

ATTENDANCE_DATA = []

ACCOUNTS_FILE = "accounts.txt"

def save_accounts_to_file():
    with open(ACCOUNTS_FILE, "w") as file:
        file.write("Saved Accounts:\n")
        for username, data in ACCOUNTS.items():
            file.write(f"Username: {username}, Password: {data['password']}, Student ID: {data['student_id']}\n")


def load_accounts_from_file():
    if not os.path.isfile(ACCOUNTS_FILE):
        return

    try:
        with open(ACCOUNTS_FILE, "r") as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()

            if not line.startswith("Username:"):
                continue

            parts = line.replace("Username: ", "").split(", ")
            username = parts[0]
            password = parts[1].replace("Password: ", "")
            student_id = parts[2].replace("Student ID: ", "")

            ACCOUNTS[username] = {
                "password": password,
                "student_id": student_id
            }
    except Exception as e:
        print(f"Error loading accounts: {e}")

def register_account():
    print("\n--- Create New Account ---")
    username = input("Enter new username: ").strip()
    if username in ACCOUNTS:
        print("Username already exists!\n")
        return

    password = input("Enter new password: ").strip()
    student_id = input("Enter student name / student ID: ").strip()

    ACCOUNTS[username] = {"password": password, "student_id": student_id}
    save_accounts_to_file()
    print(f"\nAccount '{username}' created!\n")


def edit_account():
    print("\n--- Edit Account ---")
    username = input("Enter username to edit: ").strip()

    if username not in ACCOUNTS:
        print("Account not found!\n")
        return

    print("\nLeave blank if you don't want to change that field.")

    new_username = input("New username: ").strip()
    new_password = input("New password: ").strip()
    new_student_id = input("New Student ID: ").strip()

    if new_username:
        ACCOUNTS[new_username] = ACCOUNTS.pop(username)
        username = new_username

    if new_password:
        ACCOUNTS[username]["password"] = new_password

    if new_student_id:
        ACCOUNTS[username]["student_id"] = new_student_id

    save_accounts_to_file()
    print("\nAccount updated successfully!\n")

def view_accounts():
    print("\n--- Registered Accounts ---")
    for username, info in ACCOUNTS.items():
        print(f"Username: {username} | Password: {info['password']} | Student ID: {info['student_id']}")
    print()

def delete_account():
    print("\n--- Delete Account ---")
    username = input("Enter username to delete: ").strip()

    if username not in ACCOUNTS:
        print("Account not found!\n")
        return

    if username == "admin":
        print("Cannot delete ADMIN account!\n")
        return

    del ACCOUNTS[username]
    save_accounts_to_file()
    print("\nAccount deleted successfully!\n")

def has_logged_today(student_id):
    today_str = datetime.datetime.now().strftime("%b %d, %Y")

    for entry in ATTENDANCE_DATA:
        if student_id in entry and today_str in entry:
            return True

    if os.path.isfile(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, 'r') as file:
            for line in file:
                if student_id in line and today_str in line:
                    return True
    return False

def log_attendance(student_id):
    if has_logged_today(student_id):
        print("\nYou have already logged attendance today!\n")
        return

    now = datetime.datetime.now()
    dt_string = now.strftime("%b %d, %Y - %I:%M %p")

    ATTENDANCE_DATA.append(f"User ID: {student_id} - Time: {dt_string}")
    print(f"\nAttendance marked for {student_id} at {dt_string}\n")

def view_attendance():
    print("\n--- Attendance Records ---")
    records = ATTENDANCE_DATA.copy()

    if os.path.isfile(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, 'r') as file:
            for line in file:
                if "User ID:" in line:
                    records.append(line.strip())

    if not records:
        print("No attendance records found.\n")
        return

    for r in records:
        print(r)
    print()


def save_file():
    today = datetime.date.today().strftime("%b %d, %Y")
    filename = f"Attendance Log ({today}).txt"

    
    file_exists = os.path.isfile(filename)

    with open(filename, 'a') as file:
        if not file_exists:
            file.write("Attendance Log:\n\n")

        for entry in ATTENDANCE_DATA:
            file.write(entry + "\n")

    print(f"\nAttendance log SAVED to {filename}.\n")
    ATTENDANCE_DATA.clear()

def clear_attendance():
    open(ATTENDANCE_FILE, 'w').close()
    ATTENDANCE_DATA.clear()
    print("\nAttendance log cleared!\n")
    print("Returning to login screen...\n")
    exit()  

def login():
    print("\n--- LOGIN ---")
    username = input("Enter username: ").strip()
    password = input("Enter Password: ").strip()


    if username in ACCOUNTS and ACCOUNTS[username]["password"] == password:
        print("\nLogin successful!\n")
        return username

    print("\nInvalid username or password.\n")
    return None


def manage_accounts_menu():
    while True:
        print("\n--- MANAGE ACCOUNT ---")
        print("1 - Create Account")
        print("2 - Edit Account")
        print("3 - View Accounts")
        print("4 - Delete Account")
        print("5 - Quit (Back)")
        choice = input("Choose: ").strip().upper()

        if choice == "1":
            register_account()
        elif choice == "2":
            edit_account()
        elif choice == "3":
            view_accounts()
        elif choice == "4":
            delete_account()
        elif choice == "5":
            break
        else:
            print("Invalid choice.\n")


def manage_attendance_menu():
    while True:
        print("\n--- MANAGE ATTENDANCE ---")
        print("1 - View Attendance")
        print("2 - Save Attendance")
        print("3 - Clear Attendance (Exit Program)")
        print("4 - Quit (Back)")
        choice = input("Choose: ").strip().upper()

        if choice == "1":
            view_attendance()
        elif choice == "2":
            save_file()
        elif choice == "3":
            clear_attendance()
        elif choice == "4":
            break
        else:
            print("Invalid choice.\n")


def main():
    load_accounts_from_file()
    print("--- Group 3's Python Console Attendance System ---")

    while True:
        print("\n1 - Login")
        print("2 - View Attendance List")
        print("3 - Quit")
        user_action = input("Choose: ").strip()

        if user_action == "1":
            username = login()
            if username:
                if username == "admin":
                    while True:
                        print("\n--- ADMIN MENU ---")
                        print("1 - Manage Account")
                        print("2 - Manage Attendance")
                        print("3 - Quit")
                        admin_choice = input("Choose: ").strip()

                        if admin_choice == "1":
                            manage_accounts_menu()
                        elif admin_choice == "2":
                            manage_attendance_menu()
                        elif admin_choice == "3":
                            break
                        else:
                            print("Invalid choice.\n")
                else:
                    student_id = ACCOUNTS[username]["student_id"]
                    log_attendance(student_id)

        elif user_action == "2":
            view_attendance()
        elif user_action == "3":
            print("\nExiting program...")
            break
        else:
            print("Invalid input.\n")


if __name__ == "__main__":
    main()
