import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger
import os

logger = setup_logger('db_helper')


@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306))
    )
    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    cursor.close()
    connection.close()


def fetch_expenses_for_date(expense_date, session_id):
    logger.info(f"fetch_expenses_for_date called with {expense_date} and session_id={session_id}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s AND session_id = %s", (expense_date, session_id))
        return cursor.fetchall()


def delete_expenses_for_date(expense_date, session_id):
    logger.info(f"delete_expenses_for_date called with {expense_date} and session_id={session_id}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s AND session_id = %s", (expense_date, session_id))


def delete_all_demo_data():
    logger.info("delete_all_demo_data called")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE session_id = 'demo'")


def reset_demo_data():
    logger.info("reset_demo_data called via SQL file")
    sql_path = os.path.join(os.path.dirname(__file__), "expense_db_creation.sql")
    with open(sql_path, "r") as f:
        sql_script = f.read()

    with get_db_cursor(commit=True) as cursor:
        for statement in sql_script.split(";"):
            statement = statement.strip()
            if statement:
                cursor.execute(statement)


def insert_expense(expense_date, amount, category, notes, session_id):
    logger.info(f"insert_expense with session_id={session_id}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes, session_id) VALUES (%s, %s, %s, %s, %s)",
            (expense_date, amount, category, notes, session_id)
        )


def fetch_expense_summary(start_date, end_date, session_id):
    logger.info(f"fetch_expense_summary with session_id={session_id}")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''
            SELECT category, SUM(amount) as total 
            FROM expenses 
            WHERE session_id = %s AND expense_date BETWEEN %s AND %s  
            GROUP BY category
            ''',
            (session_id, start_date, end_date)
        )
        return cursor.fetchall()


def fetch_monthly_summary(start_date, end_date, session_id):
    logger.info(f"fetch_monthly_summary with session_id={session_id}")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''
            SELECT DATE_FORMAT(expense_date, '%Y-%m') as month,
                   category,
                   SUM(amount) as total
            FROM expenses
            WHERE session_id = %s AND expense_date BETWEEN %s AND %s
            GROUP BY month, category
            ORDER BY month;
            ''',
            (session_id, start_date, end_date)
        )
        return cursor.fetchall()
