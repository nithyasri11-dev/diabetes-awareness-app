import sqlite3
import hashlib
import hmac
import os
from pathlib import Path


# =====================================================
# DATABASE CONFIGURATION
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[2]
DATABASE_PATH = BASE_DIR / "users.db"


# =====================================================
# DATABASE CONNECTION
# =====================================================

def get_connection():

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection


# =====================================================
# PASSWORD HASHING
# =====================================================

def hash_password(password, salt=None):

    if salt is None:
        salt = os.urandom(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        200000,
    )

    return salt.hex() + "$" + password_hash.hex()


def verify_password(password, stored_hash):

    try:

        salt_hex, expected_hash = stored_hash.split("$")

        salt = bytes.fromhex(salt_hex)

        actual_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            200000,
        ).hex()

        return hmac.compare_digest(
            actual_hash,
            expected_hash,
        )

    except (ValueError, TypeError):

        return False


# =====================================================
# INITIALIZE DATABASE
# =====================================================

def init_db():

    with get_connection() as connection:

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
            """
        )

        connection.commit()


# =====================================================
# REGISTER USER
# =====================================================

def register_user(name, email=None, password=None):

    # Support the old register_user(email, password) call.
    if password is None:

        password = email
        email = name
        name = email.split("@")[0]

    name = str(name).strip()
    email = str(email).strip().lower()

    if not name:

        return False, "Please enter your name."

    if not email or "@" not in email:

        return False, "Please enter a valid email address."

    if len(password) < 8:

        return False, "Password must contain at least 8 characters."

    stored_hash = hash_password(password)

    try:

        with get_connection() as connection:

            connection.execute(
                """
                INSERT INTO users (name, email, password_hash)
                VALUES (?, ?, ?)
                """,
                (name, email, stored_hash),
            )

            connection.commit()

        return True, "Account created successfully."

    except sqlite3.IntegrityError:

        return False, "An account with this email already exists."

    except sqlite3.Error:

        return False, "Unable to create the account. Please try again."


# =====================================================
# AUTHENTICATE USER
# =====================================================

def authenticate_user(email, password):

    email = str(email).strip().lower()

    try:

        with get_connection() as connection:

            user = connection.execute(
                """
                SELECT id, name, email, password_hash
                FROM users
                WHERE email = ?
                """,
                (email,),
            ).fetchone()

        if user and verify_password(
            password,
            user["password_hash"],
        ):

            return {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
            }

        return None

    except sqlite3.Error:

        return None