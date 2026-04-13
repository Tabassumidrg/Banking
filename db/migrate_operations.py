import os
import psycopg2
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)
db_url = os.environ.get('DATABASE_URL')

if not db_url:
    print("❌ Error: DATABASE_URL not found")
    exit(1)

MIGRATION_SQL = """
-- 1. Add KYC fields to users
ALTER TABLE users ADD COLUMN IF NOT EXISTS kyc_status VARCHAR(20) DEFAULT 'pending';
ALTER TABLE users ADD COLUMN IF NOT EXISTS kyc_notes TEXT;

-- 2. Create service_requests table
CREATE TABLE IF NOT EXISTS service_requests (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    type VARCHAR(50) NOT NULL,
    details TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Mark admin as verified KYC
UPDATE users SET kyc_status = 'verified' WHERE role = 'admin' OR email = 'nidhi.sharma@nidhi.bank';
"""

def run():
    print("Connecting to database for migration...")
    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cur = conn.cursor()

        print("Running migration...")
        cur.execute(MIGRATION_SQL)
        print("Migration successful!")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == "__main__":
    run()
