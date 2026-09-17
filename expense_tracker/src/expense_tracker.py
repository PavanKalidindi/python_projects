import sqlite3
from datetime import datetime
from typing import Any

class DateError(Exception):
    """Raised when an invalid date or incorrect date format is passed."""
    def __init__(self, *args):
        message = args[0] if args else 'accepted date format is "YYYY-MM-DD".'
        super().__init__(message)


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect("finance.db")
    conn.row_factory = sqlite3.Row
    conn.execute("pragma foreign_keys = on;")
    return conn


def init_db() -> None:
    with get_connection() as conn:
        cursor = conn.cursor()

        # Create categories table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                type TEXT CHECK(type IN ('expense', 'income')) NOT NULL
            );
        """)

        # Create transactions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0),
                category_id INTEGER NOT NULL,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            );
        """)


def seed_default_categories() -> None:
    categories = [
        ('Food', 'expense'),
        ('Shopping', 'expense'),
        ('Salary', 'income')
    ]

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.executemany("""
            INSERT OR IGNORE INTO categories(name, type) VALUES(?, ?)
        """, categories)


def add_category(name: str, cat_type: str = 'expense') -> None:
    """Adds a new category to categories table."""
    if not name.strip():
        raise ValueError("Category name cannot be empty.")

    if cat_type not in ('expense', 'income'):
        raise ValueError("cat_type must be 'expense' or 'income'.")

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO categories(name, type) VALUES(?, ?)
        """, (name.strip(), cat_type))


def validate_date(date: str, format: str = "%Y-%m-%d") -> bool:
    try:
        datetime.strptime(date, format)
        return True
    except ValueError:
        return False


def validate_option(option: str) -> bool:
    return option in ['month', 'year']


def add_transaction(date: str, amount: int | float, category: str) -> None:
    """Adds the transaction to finance.db."""
    if not validate_date(date):
        raise DateError()

    if amount <= 0:
        raise ValueError('Amount must be strictly greater than zero.')

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM categories WHERE name = ?", (category,))
        row = cursor.fetchone()

        if not row:
            # Fetch available categories for helpful error messaging
            cursor.execute("SELECT name FROM categories")
            available = [r["name"] for r in cursor.fetchall()]
            raise ValueError(f"Invalid category '{category}'. Choose from {available}")

        category_id = row["id"]

        cursor.execute(
            "INSERT INTO transactions(date, amount, category_id) VALUES(?, ?, ?)",
            (date, amount, category_id)
        )


def generate_summary(option: str) -> list[dict[str, Any]]:
    if not validate_option(option):
        raise ValueError("Option must be either 'month' or 'year'")

    now = datetime.now()
    if option == 'month':
        date_filter = now.strftime('%Y-%m')
        strftime_format = "%Y-%m"
    else:
        date_filter = now.strftime('%Y')
        strftime_format = "%Y"

    query = """
    WITH category_spendings AS (
        SELECT 
            c.name AS category, 
            SUM(t.amount) AS spent
        FROM transactions t
        JOIN categories c ON c.id = t.category_id
        WHERE strftime(?, t.date) = ? AND c.type = 'expense'
        GROUP BY c.id, c.name
    )
    SELECT
        category,
        spent,
        ROUND((spent / SUM(spent) OVER() * 100), 2) AS spent_percentage
    FROM category_spendings
    ORDER BY spent DESC;
    """

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (strftime_format, date_filter))
        return [dict(row) for row in cursor.fetchall()]