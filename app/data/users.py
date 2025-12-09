import pandas as pd
from app.data.db import connect_database
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)
def insert_user(username, password_hash, role='user'):
    """Insert new user."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users 
        (username, password_hash, role)
        VALUES (?, ?, ?)
    """, (username, password_hash, role))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id

def get_all_users():
    """Get all users as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM users ORDER BY id DESC",
        conn
    )
    conn.close()
    return df

def delete_user(conn, user_id):
    """
    Delete a user from the database.
    """
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    return cursor.rowcount

def update_user_role(conn, user_id, new_role):
    """
    Update the role of a user.
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))
    conn.commit()
    return cursor.rowcount


def get_user_by_username(username):
    """
    Retrieve a single user by their username.
    Returns: A tuple (id, username, password_hash, role) or None.
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, password_hash, role FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()
    conn.close()
    return user