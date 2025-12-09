import pandas as pd
from app.data.db import connect_database

def insert_ticket(title, description, priority='medium', status='open', category=None, created_by=None, assigned_to=None, resolution_notes=None):
    """Insert new IT ticket."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO it_tickets 
        (title, description, priority, status, category, created_by, assigned_to, resolution_notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (title, description, priority, status, category, created_by, assigned_to, resolution_notes))
    conn.commit()
    ticket_id = cursor.lastrowid
    conn.close()
    return ticket_id

def get_all_tickets():
    """Get all IT tickets as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM it_tickets ORDER BY id DESC",
        conn
    )
    conn.close()
    return df

def delete_ticket(conn, ticket_id):
    """
    Delete an IT ticket from the database.
    """
    cursor = conn.cursor()
    cursor.execute("DELETE FROM it_tickets WHERE id = ?", (ticket_id,))
    conn.commit()
    return cursor.rowcount

def update_ticket_status(conn, ticket_id, new_status):
    """
    Update the status of an IT ticket.
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE it_tickets SET status = ? WHERE id = ?", (new_status, ticket_id))
    conn.commit()
    return cursor.rowcount
