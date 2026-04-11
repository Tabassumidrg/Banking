"""
Full database setup + admin account creation.
Run this to initialize the DB from scratch and create the admin user.
"""
import os
import psycopg2
import bcrypt
from dotenv import load_dotenv

# Load from the local .env file
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)
db_url = os.environ.get('DATABASE_URL')

if not db_url:
    print("❌ Error: DATABASE_URL not found in db/.env")
    exit(1)

# Admin credentials to set
ADMIN_EMAIL    = "admin@nidhi.bank"
ADMIN_PASSWORD = "Admin@1234"
ADMIN_NAME     = "Bank Administrator"
ADMIN_MOBILE   = "9000000001"

CREATE_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    mobile_number VARCHAR(20) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    balance DECIMAL(12,2) DEFAULT 1000.00,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    sender_id INTEGER REFERENCES users(id),
    receiver_id INTEGER REFERENCES users(id),
    amount DECIMAL(12,2) NOT NULL,
    type VARCHAR(20) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'success',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
"""

def run():
    print("🔗 Connecting to Neon PostgreSQL...")
    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cur = conn.cursor()

        print("📦 Creating tables (if not exist)...")
        cur.execute(CREATE_SQL)
        print("   ✅ Tables ready.")

        # Add role column if it's missing (for existing DBs)
        try:
            cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(20) DEFAULT 'user'")
        except Exception:
            pass

        # Add full_name column if missing
        try:
            cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS full_name VARCHAR(255)")
        except Exception:
            pass

        print("👤 Creating admin account...")
        hashed = bcrypt.hashpw(ADMIN_PASSWORD.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        cur.execute("""
            INSERT INTO users (full_name, email, mobile_number, password_hash, balance, role)
            VALUES (%s, %s, %s, %s, %s, 'admin')
            ON CONFLICT (email) DO UPDATE
            SET password_hash = EXCLUDED.password_hash,
                role           = 'admin',
                full_name      = EXCLUDED.full_name
            RETURNING id, email, role
        """, (ADMIN_NAME, ADMIN_EMAIL, ADMIN_MOBILE, hashed, 0.0))

        row = cur.fetchone()

        print(f"\n{'='*50}")
        print(f"✅ SUCCESS! Management Portal Credentials:")
        print(f"   Email    : {ADMIN_EMAIL}")
        print(f"   Password : {ADMIN_PASSWORD}")
        print(f"   Role     : {row[2]}")
        print(f"   DB ID    : {row[0]}")
        print(f"{'='*50}\n")
        print("Go to your bank site → Login → 'Management Portal'")
        print("Use the credentials above to sign in.\n")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run()
