from pathlib import Path
import re
import sqlite3

from argon2 import PasswordHasher
from argon2.exceptions import (
    VerifyMismatchError,
    VerificationError
)

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_DIR = BASE_DIR / "database"
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_PATH = DATABASE_DIR / "users.sqlite3"

password_hasher = PasswordHasher()


def init_db():
    """Create the users table if it does not exist."""

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.commit()


def register_user(email, password):
    """Register a new user with a hashed password."""

    email = (email or "").strip().lower()

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return False, "Please enter a valid email address."

    if len(password or "") < 10:
        return False, "Password must contain at least 10 characters."

    password_hash = password_hasher.hash(password)

    try:
        with sqlite3.connect(DATABASE_PATH) as connection:
            connection.execute(
                """
                INSERT INTO users (email, password_hash)
                VALUES (?, ?)
                """,
                (email, password_hash)
            )

            connection.commit()

        return True, "Account created successfully."

    except sqlite3.IntegrityError:
        return False, "This email is already registered."


def authenticate_user(email, password):
    """Verify the user's credentials."""

    email = (email or "").strip().lower()

    with sqlite3.connect(DATABASE_PATH) as connection:
        user = connection.execute(
            """
            SELECT id, email, password_hash
            FROM users
            WHERE email = ?
            """,
            (email,)
        ).fetchone()

    if user is None:
        return None

    try:
        password_hasher.verify(user[2], password or "")

        return {
            "id": user[0],
            "email": user[1]
        }

    except (
        VerifyMismatchError,
        VerificationError,
        ValueError
    ):
        return None