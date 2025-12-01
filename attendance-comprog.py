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


# ---------- ACCOUNT SYSTEM ----------

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

    save_accounts_to_file()
    print(f"Account created for user '{username}'!\n")


# ---------- ATTENDANCE SYSTEM ----------

def has_logged_today(student_id):
    """Prevent duplicate logs (checks both memory and file)."""
    today_str = datetime.datetime.now().strftime("%b %d, %Y")

    # Check unsaved in-memory logs
    for entry in ATTENDANCE_DATA:
        if student_id in entry and today_str in entry:
            return True

    # Check saved file logs
    if os.path.isfile(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith("User ID:") and student_id in line and today_str in line:
                    return True

    return False


def log_attendance(student_id):

    if has_logged_today(student_id):
        print("\nYou have already logged attendance today!\n")
        return

    now = datetime.datetime.now()
    dt_string = now.strftime("%b %d, %Y - %I:%M %p")

    ATTENDANCE_DATA.append(f"User ID: {student_id} - Time: {dt_string}")
    print(f"\nAttendance marked for Student {student_id} at {dt_string}\n")


def view_attendance():
    print("\n--- Attendance Records ---")

    records = []

    # Add unsaved in-memory logs
    for entry in ATTENDANCE_DATA:
        records.append(entry)

    # Add saved logs from file
    if os.path.isfile(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith("User ID:"):
                    records.append(line)

    # Remove duplicates
    records = list(dict.fromkeys(records))

    if not records:
        print("No attendance records found.\n")
        return
    
    def extract_datetime(record):
        try:
            # Extract the actual datetime from the text
            time_part = record.split("Time: ")[1]
            return datetime.datetime.strptime(time_part, "%b %d, %Y - %I:%M %p")
        except:
            return datetime.datetime.min  # fallback if parsing fails

    records.sort(key=extract_datetime)

    for r in records:
        print(r)

    print()


def save_file():
    #today = datetime.date.today().strftime("%b %d, %Y")

    write_header = not os.path.isfile(ATTENDANCE_FILE) or os.path.getsize(ATTENDANCE_FILE) == 0

    with open(ATTENDANCE_FILE, 'w') as file:
        file.write("Attendance Log:\n\n")

        #if write_header:
            #file.write(f"Saved attendance records on {today}:\n")

        for entry in ATTENDANCE_DATA:
            file.write(entry + "\n")

    print(f"\nAttendance log saved to {ATTENDANCE_FILE}.\n")
    #ATTENDANCE_DATA.clear()



def clear_attendance():
    open(ATTENDANCE_FILE, 'w').close()
    ATTENDANCE_DATA.clear()
    print("\nAttendance log cleared!\n")


def after_view_attendance():
    while True:
        print("1 - Save the file")
        print("2 - Back")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            save_file()
            print(f"\nAttendance log saved as {ATTENDANCE_FILE}.\n")
            break
        elif choice == "2":
            break
        else:
            print("Invalid choice. Try again.\n")


# ---------- MENUS ----------

def login():
    print("\n--- LOGIN ---")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    if username in ACCOUNTS and ACCOUNTS[username]["password"] == password:
        print("\nLogin successful!\n")
        return username

    print("\nInvalid username or password.\n")
    return None


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
            after_view_attendance()
        elif admin_choice == "3":
            clear_attendance()
        elif admin_choice == "4":
            register_account()
        elif admin_choice == "5":
            print("\nAdmin logged out.\n")
            break
        else:
            print("Invalid choice. Try again.\n")


# ---------- MAIN PROGRAM ----------

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


# ---------- START PROGRAM ----------

if __name__ == "__main__":
    load_accounts_from_file()
    main()
