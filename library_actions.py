from database import run_query
from tabulate import tabulate


def issue_book(student_id, book_name):
    try:
        run_query(
            "INSERT INTO book_issues(student_id, book_name) VALUES(%s, %s)",
            (student_id, book_name)
        )
    
    except Exception as e:
        result = {
            "success": False,
            "message": f"[ERROR]: {e}"
        }
    
    else: 
        result = {
            "success": True,
            "message": f"Book issue successfull"
        }

    finally:
        return result

def view_all_issues():
    try:
        res = run_query("SELECT * FROM book_issues", fetch=True)
    except Exception as e:
        result = {
            "success": False,
            "message": f"[ERROR]: {e}"
        }
    else: 
        result = {
            "success": True,
            "message": f"fetched book issues",
            "data": res
        }
    finally:
        return result

def return_book(issue_id):
    try:
        run_query(
            "UPDATE book_issues SET status='returned', return_date = CURRENT_DATE WHERE issue_id=%s",
            (issue_id,)
        )
    except Exception as e:
        result = {
            "success": False,
            "message": f"[ERROR]: {e}"
        }
    else:
        result = {
            "success": True,
            "message": f"Book issue with issue ID: {issue_id} returned"
        }
    finally:
        return result

def view_my_books(student_id):
    try:
        res = run_query(
            "SELECT * FROM book_issues WHERE student_id=%s",
            (student_id,),
            fetch=True
        )
    except Exception as e:
        result = {
            "success": False,
            "message": f"[ERROR]: {e}"
        }
    else:
        result = {
            "success": True,
            "message": f"Fetched all book issues by student (id: {student_id})",
            "data": res
        }
    finally:
        return result