from tabulate import tabulate
from database import initialize_database, get_connection, run_query
from library_actions import  view_all_issues
import time

from auth import login, register
from library_actions import view_my_books, issue_book, return_book


def auth_ui(role):
    print("\nPlease identify yourself:\n1. Login\n2. Register")
    ch = int(input("\nEnter Choice: "))
    
    if ch == 1:
        username = input("\nEnter Username: ")
        password = input("\nEnter Password: ")

        res = login(role, username, password)
        if res["success"]:
            print(res["message"])
            if role == "manager": init_manager_ui(res["data"]) 
            else: init_student_ui(res["data"])
        else:
            print("No records with that username/passwrod")
            main_ui()
    
    if ch == 2:
        name = input("\nEnter your name: ")
        username = input(f"Enter a unique username (e.g.{name.lower().replace(' ', '_')}): ")
        password = input("\nEnter Password: ")

        res = register(role, username, password, name)
        print(res["message"])

        main_ui()

def init_manager_ui(manager_obj):
    print("1. Issue a book to a student\n2. Record Book Return\n3. View All Issued Records\n4. Logout")
    ch = int(input("\nEnter Choice: "))

    if ch == 1:
        students = run_query(
            "SELECT student_id, name, username FROM students",
            fetch=True
        )
        print(f"All Students: \n{tabulate(students, headers=['Student ID', 'Name', 'Username'])}") if len(students) else print("You have currently no students enrolled...")

        student_id = int(input("\nEnter Student ID: "))
        book_name = str(input("\nBook Name: ")).lower()

        res = issue_book(student_id, book_name)
        print(f"\n{res["message"]}")
        init_manager_ui(manager_obj)
    
    if ch == 2:
        issues = run_query(
            "SELECT * FROM book_issues",
            fetch=True
        )
        print(f"\nAll book issues: \n{tabulate(issues, headers=['Issue ID', 'Student ID', 'Book Name', 'Issue Date', 'Return Date', 'Status'])}") if len(issues) else print("You have currently no book issues...")

        issues_id = int(input("\nEnter Issue ID: "))
        res = return_book(issues_id)
        print(res["message"])
        init_manager_ui(manager_obj)
    
    if ch == 3:
        issues = view_all_issues()
        issues_data = issues.get("data", []) if issues.get("success") else []
        print(f"\nAll issues: \n{tabulate(issues_data, headers=['Issue ID', 'Student ID', 'Book Name', 'Issue Date', 'Return Date', 'Status'])}") if len(issues_data) else print("You have currently no book issues...")
        init_manager_ui(manager_obj)

    elif ch == 4:
        manager_obj = None
        print("Logging out...")
        main_ui()
    else: 
        main_ui()


def init_student_ui(student_obj):
    student_id = student_obj[0] 

    print(f"\nWelcome {student_obj[1]}")
    print("Your Options:\n1. View My Issued Books\n2. Logout")
    ch = int(input("\nEnter Choice: "))

    if ch == 1:
        res = view_my_books(student_id)
        books_data = res.get("data", []) if res.get("success") else []
        print(tabulate(books_data, headers=['Issue ID', 'Student ID', 'Book Name', 'Issue Date', 'Return Date', 'Status'])) if len(books_data) else print("You have no issued books...")
        init_student_ui(student_obj)
    
    elif ch == 2:
        student_id = None
        print("Logging out...")
        main_ui()

def main_ui():
    print("\n\n--LIBRARY MANAGEMENT--")

    print("\nPlease select your role\n1. Manager\n2. Student")
    ch = int(input("\nEnter Choice: "))

    if ch == 1:
        auth_ui(role="manager")
    elif ch == 2:
        auth_ui(role="student")
    else:
        print("Shutting down tool...")
        time.sleep(1)
        exit()
    
if __name__ == "__main__":
    conn = get_connection(use_database=False)
    try:
        initialize_database(conn)
    finally:
        conn.close()
    main_ui()