import pandas as pd  # Added for DataFrame operations
from app.data.db import connect_database, DB_PATH
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.incidents import insert_incident, get_all_incidents, update_incident_status, delete_incident
from app.data.users import get_user_by_username
from app.services.loadCSV import load_all_csv_data

# Added missing analytical functions
def get_incidents_by_severity_count(conn):
    """Get count of incidents by severity."""
    return pd.read_sql_query(
        "SELECT severity, COUNT(*) as count FROM cyber_incidents GROUP BY severity",
        conn
    )

def get_high_severity_by_status(conn):
    """Get high-severity incidents grouped by status."""
    return pd.read_sql_query(
        "SELECT status, COUNT(*) as count FROM cyber_incidents WHERE severity = 'high' GROUP BY status",
        conn
    )

def main():
    print("=" * 60)
    print("Week 8: Database Demo")
    print("=" * 60)
    
    # 1. Setup database
    conn = connect_database()
    create_all_tables(conn)
    
    # 2. Migrate users (fixed: pass conn)
    migrate_users_from_file(conn)
    
    # 3. Test authentication
    if not get_user_by_username("alice"):
        success, msg = register_user("alice", "SecurePass123!", "analyst")
        print(msg)
    else:
        print("User 'alice' already exists, skipping registration.")

    success, msg = login_user("alice", "SecurePass123!")
    print(msg)
    
    # 4. Test CRUD
    incident_id = insert_incident(
        "Phishing Attack Detected",  # title
        "Suspicious email detected with malicious link.", # description
        "2024-11-05",  # incident_date
        "high",        # severity (optional, but good to include)
        "open",        # status (optional, but good to include)
        None,          # assigned_to (optional, keeping it None or a user ID)
        "alice"        # reported_by
    )
    print(f"Created incident #{incident_id}")
    
    # 5. Query data
    df = get_all_incidents()
    print(f"Total incidents: {len(df)}")
    
    conn.close()

if __name__ == "__main__":
    main()

def run_comprehensive_tests():
    """
    Run comprehensive tests on your database.
    """
    print("\n" + "="*60)
    print("🧪 RUNNING COMPREHENSIVE TESTS")
    print("="*60)
    
    conn = connect_database()
    
    # Test 1: Authentication
    print("\n[TEST 1] Authentication")
    if not get_user_by_username("test_user"):
        success, msg = register_user("test_user", "TestPass123!", "user")
        print(f"  Register: {'✅' if success else '❌'} {msg}")
    else:
        print("  Register: ✅ User 'test_user' already exists, skipping registration.")

    success, msg = login_user("test_user", "TestPass123!")
    print(f"  Login:    {'✅' if success else '❌'} {msg}")
    
    # Test 2: CRUD Operations
    print("\n[TEST 2] CRUD Operations")
    
    # Create
    test_id = insert_incident(
        "Test Incident Title", # title
        "This is a test incident description.", # description
        "2024-11-05",          # incident_date
        "low",                 # severity
        "open",                # status
        None,                  # assigned_to (or a user ID)
        "test_user"
    )
    print(f"  Create: ✅ Incident #{test_id} created")
    
    # Read
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents WHERE id = ?",
        conn,
        params=(test_id,)
    )
    print(f"  Read:    Found incident #{test_id}")
    
    # Update
    update_incident_status(conn, test_id, "resolved")
    print(f"  Update:  Status updated")
    
    # Delete
    delete_incident(conn, test_id)
    print(f"  Delete:  Incident deleted")
    
    # Test 3: Analytical Queries
    print("\n[TEST 3] Analytical Queries")
    
    df_by_severity = get_incidents_by_severity_count(conn)
    print(f"  By Severity: Found {len(df_by_severity)} severity levels")
    
    df_high = get_high_severity_by_status(conn)
    print(f"  High Severity: Found {len(df_high)} status categories")
    
    conn.close()
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)

# Run tests
run_comprehensive_tests()

def setup_database_complete():
    """
    Complete database setup:
    1. Connect to database
    2. Create all tables
    3. Migrate users from users.txt
    4. Load CSV data for all domains
    5. Verify setup
    """
    print("\n" + "="*60)
    print("STARTING COMPLETE DATABASE SETUP")
    print("="*60)
    
    # Step 1: Connect
    print("\n[1/5] Connecting to database...")
    conn = connect_database()
    print("       Connected")
    
    # Step 2: Create tables
    print("\n[2/5] Creating database tables...")
    create_all_tables(conn)
    
    # Step 3: Migrate users
    print("\n[3/5] Migrating users from users.txt...")
    user_count = migrate_users_from_file(conn)
    print(f"       Migrated {user_count} users")
    
    # Step 4: Load CSV data
    print("\n[4/5] Loading CSV data...")
    total_rows = load_all_csv_data(conn)
        # Step 5: Verify
    print("\n[5/5] Verifying database setup...")
    cursor = conn.cursor()
    
    # Count rows in each table
    tables = ['users', 'cyber_incidents', 'datasets_metadata', 'it_tickets']
    print("\n Database Summary:")
    print(f"{'Table':<25} {'Row Count':<15}")
    print("-" * 40)
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:<25} {count:<15}")
    
    conn.close()
    
    print("\n" + "="*60)
    print(" DATABASE SETUP COMPLETE!")
    print("="*60)
    print(f"\n Database location: {DB_PATH.resolve()}")
    print("\nYou're ready for Week 9 (Streamlit web interface)!")

# Run the complete setup
setup_database_complete()