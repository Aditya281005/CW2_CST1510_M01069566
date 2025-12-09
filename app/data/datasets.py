import pandas as pd
from app.data.db import connect_database

def insert_dataset(name, description, source, data_type='raw', classification='internal', created_by=None, file_path=None, size_bytes=None):
    """Insert new dataset metadata."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata 
        (name, description, source, data_type, classification, created_by, file_path, size_bytes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, description, source, data_type, classification, created_by, file_path, size_bytes))
    conn.commit()
    dataset_id = cursor.lastrowid
    conn.close()
    return dataset_id

def get_all_datasets():
    """Get all datasets metadata as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM datasets_metadata ORDER BY id DESC",
        conn
    )
    conn.close()
    return df

def delete_dataset(conn, dataset_id):
    """
    Delete a dataset metadata entry from the database.
    """
    cursor = conn.cursor()
    cursor.execute("DELETE FROM datasets_metadata WHERE id = ?", (dataset_id,))
    conn.commit()
    return cursor.rowcount

def update_dataset_classification(conn, dataset_id, new_classification):
    """
    Update the classification of a dataset metadata entry.
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE datasets_metadata SET classification = ? WHERE id = ?", (new_classification, dataset_id))
    conn.commit()
    return cursor.rowcount
