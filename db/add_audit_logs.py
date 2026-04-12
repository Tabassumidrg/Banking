import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="d:\\saif\Banking\\db\\.env")
db_url = os.environ.get("DATABASE_URL")

if not db_url:
    print("Error: DATABASE_URL not found")
    exit(1)

CREATE_AUDIT_LOGS_TABLE = """
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    details TEXT,
    ip_address VARCHAR(45),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
"""

def migrate():
    print("Connecting to database...")
    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cur = conn.cursor()
        
        print("Creating audit_logs table...")
        cur.execute(CREATE_AUDIT_LOGS_TABLE)
        
        print("Migration complete!")
    except Exception as e:
        print(f"Migration error: {e}")
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    migrate()
