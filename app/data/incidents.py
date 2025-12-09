import pandas as pd
from app.data.db import connect_database

def insert_incident(title, description, incident_date, severity='medium', status='open', assigned_to=None, reported_by=None):
    """Insert new incident."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cyber_incidents 
        (title, description, incident_date, severity, status, assigned_to, reported_by)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title, description, incident_date, severity, status, assigned_to, reported_by))
    conn.commit()
    incident_id = cursor.lastrowid
    conn.close()
    return incident_id

def get_all_incidents():
    """Get all incidents as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents ORDER BY id DESC",
        conn
    )
    conn.close()
    return df

def delete_incident(conn, incident_id):
    """
    Delete an incident from the database.
    """
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cyber_incidents WHERE id = ?", (incident_id,))
    conn.commit()
    return cursor.rowcount

def update_incident_status(conn, incident_id, new_status):
    """
    Update the status of an incident.
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE cyber_incidents SET status = ? WHERE id = ?", (new_status, incident_id))
    conn.commit()
    return cursor.rowcount
