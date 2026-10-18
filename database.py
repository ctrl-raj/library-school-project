import os 
import mysql.connector
from dotenv import load_dotenv

load_dotenv()
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

def get_connection(use_database=True):
    try: 
        conn = mysql.connector.connect(
            host="localhost",
            user=db_user,
            password=db_password,
            database=db_name if use_database else None
        )
    except Exception as e:
        print(f"[CONNECTION ERROR]: {e}", flush=True)
        exit()
    else:
        return conn

def run_query(query, params=(), fetch=False):
    conn = get_connection()
    cursor = None

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        if fetch:
            return cursor.fetchall()
        conn.commit()
    finally:
        try:
            if cursor is not None:
                cursor.close()
        finally:
            conn.close()

def initialize_database(conn):
    cursor = conn.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.execute(f"USE {db_name}")

        cursor.execute(f"""CREATE TABLE IF NOT EXISTS managers(
                manager_id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(50) NOT NULL,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)

        cursor.execute(f"""CREATE TABLE IF NOT EXISTS students(
                student_id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(50) NOT NULL,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL
            )
        """)

        cursor.execute(f"""CREATE TABLE IF NOT EXISTS book_issues(
                issue_id INT PRIMARY KEY AUTO_INCREMENT,
                student_id INT NOT NULL,
                book_name VARCHAR(150) NOT NULL,
                issue_date DATE NOT NULL DEFAULT (CURRENT_DATE),
                return_date DATE,
                status ENUM('issued', 'returned') NOT NULL DEFAULT 'issued',
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            )
        """)

    finally:
        cursor.close()