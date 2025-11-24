import datetime
import csv
import os

# Stores accounts in memory
# Format:
# username : { "password": ..., "student_id": ... }
ACCOUNTS = {
    "admin": {
        "password": "admin123",  # Fixed admin password
        "student_id": "Administrator"
    }
}

ATTENDANCE_FILE = 'attendance_log.csv'


def register_account():
    print("\n--- Register New Account ---")

    username = input("Enter new username: ").strip()
    if username in ACCOUNTS:
        print("Username already exists!\n")
        return

    password = input("Enter new password: ").strip()
    student_id = input("Enter student name / student ID: ").strip()

    ACCOUNTS[username] = {
        "password": password,
        "student_id": student_id
    }

    print(f"Account created for user '{username}'!\n")


def log_attendance(student_id):
    now = datetime.datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

    file_exists = os.path.isfile(ATTENDANCE_FILE)

    try:
        with open(ATTENDANCE_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['User ID', 'Timestamp'])
            writer.writerow([student_id, dt_string])
        print(f"Attendance marked for Student {student_id} at {dt_string}\n")
    except IOError as e:
        print(f"Error writing to file: {e}")


def login():
    print("\n--- LOGIN ---")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    if username in ACCOUNTS and ACCOUNTS[username]["password"] == password:
        print("Login successful!\n")
        return username  # Return username instead of student_id
    else:
        print("Invalid username or password.\n")
        return None


def view_attendance():
    print("\n--- Attendance Records ---")

    if not os.path.isfile(ATTENDANCE_FILE):
        print("No attendance records found.\n")
        return

    try:
        with open(ATTENDANCE_FILE, mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)

            if len(rows) <= 1:
                print("\nAttendance log is currently empty.\n")
                return

            for row in rows:
                print(f"User ID: {row[0]} | Time: {row[1]}")
            print()
    except IOError as e:
        print(f"Error reading file: {e}\n")


def clear_attendance():
    with open(ATTENDANCE_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['User ID', 'Timestamp'])
    print("\nAttendance log cleared!\n")


def view_accounts():
    print("\n--- Registered Accounts ---")
    for username, info in ACCOUNTS.items():
        print(f"Username: {username} | Password: {info['password']} | Student ID: {info['student_id']}")
    print()


def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1 - View all accounts")
        print("2 - View attendance list")
        print("3 - Clear attendance log")
        print("4 - Register new account")
        print("5 - Logout")
        admin_choice = input("Choose an option: ").strip()

        if admin_choice == "1":
            view_accounts()
        elif admin_choice == "2":
            view_attendance()
        elif admin_choice == "3":
            clear_attendance()
        elif admin_choice == "4":
            register_account()
        elif admin_choice == "5":
            print("Admin logged out.\n")
            break
        else:
            print("Invalid choice. Try again.\n")


def main():
    print("--- Group 3's Python Console Attendance System ---")

    while True:
        print("\nOptions:")
        print("1 - Login and log attendance")
        print("2 - View attendance list")
        print("3 - Quit")

        user_action = input("Choose an option (1/2/3): ").strip()

        if user_action == "1":
            username = login()
            if username:
                if username == "admin":
                    admin_menu()
                else:
                    student_id = ACCOUNTS[username]["student_id"]
                    log_attendance(student_id)

        elif user_action == "2":
            view_attendance()

        elif user_action == "3":
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Try again.\n")


if __name__ == "__main__":
    main()
