import datetime
import csv
import os

# username : { password, student_id }
ACCOUNTS = {
    "Roberto": {"password": "roberto123", "student_id": "Kris"},
    "Silva": {"password": "silva123", "student_id": "Danielle"},
    "Perez": {"password": "perez123", "student_id": "Frank"},
}
ATTENDANCE_FILE = 'attendance_log.csv'

def log_attendance(student_id):
    now = datetime.datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S") # ewan ko sir nakita ko lang sa internet hehe

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
    print("\n--- LOGIN pls ---")

    username = input("Enter username: ")
    password = input("Enter password: ")

    if username in ACCOUNTS and ACCOUNTS[username]["password"] == password:
        print("Login successful!\n")
        return ACCOUNTS[username]["student_id"]
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

def main():
    print("--- Group 3's Python Console Attendance System ---")

    while True:
        print("Options:")
        print("1 - Login and log attendance")
        print("2 - View attendance list")
        print("3 - Clear attendance log")
        print("4 - Quit")
        
        user_action = input("Choose an option (1/2/3/4): ")

        if user_action == "1":
            student_id = login()
            if student_id:
                log_attendance(student_id)

        elif user_action == "2":
            view_attendance()

        elif user_action == "3":
            clear_attendance()
        
        elif user_action == "4":
            print("Exiting program...")
            break  

        else:
            print("Invalid choice. Try again.\n")
            
            
def clear_attendance():
    with open(ATTENDANCE_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['User ID', 'Timestamp'])  # Write fresh header
    print("\nAttendance log cleared!\n")

if __name__ == "__main__":
    main()
