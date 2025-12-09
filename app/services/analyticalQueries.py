import pandas as pd  # Ensure pandas is imported
from app.data.db import connect_database  

def get_incidents_by_type_count(conn):
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_high_severity_by_status(conn):
    query = """
    SELECT status, COUNT(*) as count
    FROM cyber_incidents
    WHERE severity = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_incident_types_with_many_cases(conn, min_count=5):
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    HAVING COUNT(*) >= ?
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_count,))
    return df

# Test: Run analytical queries
conn = connect_database()

print("\n Incidents by Type:")
df_by_type = get_incidents_by_type_count(conn)
print(df_by_type)

print("\n High Severity Incidents by Status:")
df_high_severity = get_high_severity_by_status(conn)
print(df_high_severity)

print("\n Incident Types with Many Cases (>5):")
df_many_cases = get_incident_types_with_many_cases(conn, min_count=5)
print(df_many_cases)

conn.close()
                                            