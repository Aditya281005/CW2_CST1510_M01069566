
def create_users_table(conn):
    """Create users table."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Add index for faster lookups by username
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)")
    conn.commit()

def create_cyber_incidents_table(conn):
    """Create cyber incidents table for tracking security events."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            incident_date DATETIME NOT NULL,
            severity TEXT CHECK(severity IN ('low', 'medium', 'high', 'critical')) DEFAULT 'medium',
            status TEXT CHECK(status IN ('open', 'investigating', 'resolved', 'closed')) DEFAULT 'open',
            assigned_to INTEGER,
            reported_by INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (assigned_to) REFERENCES users(id),
            FOREIGN KEY (reported_by) REFERENCES users(id)
        )
    """)
    # Add indexes for common queries
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cyber_incidents_status ON cyber_incidents(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cyber_incidents_incident_date ON cyber_incidents(incident_date)")
    conn.commit()

def create_datasets_metadata_table(conn):
    """Create datasets metadata table for managing intelligence datasets."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            source TEXT,
            data_type TEXT CHECK(data_type IN ('raw', 'processed', 'aggregated')) DEFAULT 'raw',
            classification TEXT CHECK(classification IN ('public', 'internal', 'confidential', 'restricted')) DEFAULT 'internal',
            created_by INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
            file_path TEXT,
            size_bytes INTEGER,
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    """)
    # Add indexes for common queries
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_datasets_metadata_name ON datasets_metadata(name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_datasets_metadata_classification ON datasets_metadata(classification)")
    conn.commit()

def create_it_tickets_table(conn):
    """Create IT tickets table for tracking support requests."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT CHECK(priority IN ('low', 'medium', 'high', 'urgent')) DEFAULT 'medium',
            status TEXT CHECK(status IN ('open', 'in_progress', 'resolved', 'closed')) DEFAULT 'open',
            category TEXT,
            created_by INTEGER,
            assigned_to INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            resolution_notes TEXT,
            FOREIGN KEY (created_by) REFERENCES users(id),
            FOREIGN KEY (assigned_to) REFERENCES users(id)
        )
    """)
    # Add indexes for common queries
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_it_tickets_status ON it_tickets(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_it_tickets_priority ON it_tickets(priority)")
    conn.commit()

def create_all_tables(conn):
    """Create all tables."""
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)
