import bcrypt
from pathlib import Path
from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user
import sqlite3

def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    password_bytes = plain_text_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def register_user(username, password, role='user'):
    """Register new user with password hashing."""
    # Hash password
    password_hash = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')
    
    # Insert into database
    insert_user(username, password_hash, role)
    return True, f"User '{username}' registered successfully."

def login_user(username, password):
    """Authenticate user."""
    user = get_user_by_username(username)
    if not user:
        return False, "User not found."
    
    # Verify password
    stored_hash = user[2]  # password_hash column
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return True, f"Login successful!"
    return False, "Incorrect password."


def migrate_users_from_file(conn, filepath=Path("DATA") / "users.txt"):

    if not filepath.exists():
        print(f" File not found: {filepath}")
        print("   No users to migrate.")
        return

    conn = connect_database()
    cursor = conn.cursor()
    migrated_count = 0
    valid_roles = ['user', 'admin', 'analyst']

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Parse line: username,password_hash,role
            parts = line.split(',')
            if len(parts) >= 2:
                username = parts[0]
                password_hash = parts[1]
                role = parts[2] if len(parts) >= 3 and parts[2] in valid_roles else 'user'  # Default to 'user' if invalid/missing

                # Insert user (ignore if already exists)
                try:
                    cursor.execute(
                        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                        (username, password_hash, role)
                    )
                    if cursor.rowcount > 0:
                        migrated_count += 1
                except sqlite3.Error as e:
                    print(f"Error migrating user {username}: {e}")

    conn.commit()
    print(f"✅ Migrated {migrated_count} users from {filepath.name}")

    cursor = conn.cursor()


    cursor.execute("SELECT id, username, role FROM users")
    users = cursor.fetchall()

    print(" Users in database:")
    print(f"{'ID':<5} {'Username':<15} {'Role':<10}")
    print("-" * 35)
    for user in users:
        print(f"{user[0]:<5} {user[1]:<15} {user[2]:<10}")

    print(f"\nTotal users: {len(users)}")
    conn.close()
    return migrated_count

def user_exists(userName):
    conn = connect_database()
    if not conn:
        return False
    
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (userName,))
        user = cursor.fetchone()
        return user is not None

    except sqlite3.Error as e:
        print(f"Error checking user existence: {e}")
        return False

    finally:
        conn.close()


def special_character(c):
    return not c.isalnum()

def check_password_strength(password) -> tuple[bool, str]:
    if len(password) < 8:
        return (False, "Password must be at least 8 characters long.")

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(special_character(c) for c in password)

    if not has_upper:
        return (False, "Password must contain an uppercase letter.")
    if not has_lower:
        return (False, "Password must contain a lowercase letter.")
    if not has_digit:
        return (False, "Password must contain a digit.")
    if not has_special:
        return (False, "Password must contain a special character.")

    return (True, "Password is strong.")


def validate_password(password):
    return check_password_strength(password)
