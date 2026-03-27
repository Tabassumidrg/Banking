import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
dotenv_path = r"d:\saif\Banking\db\.env"
load_dotenv(dotenv_path=dotenv_path)
db_url = os.environ.get("DATABASE_URL")

if not db_url:
    print("Error: DATABASE_URL not found")
    exit(1)

def migrate():
    print("Connecting to database...")
    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cur = conn.cursor()
        
        print("Adding balance column to users...")
        cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS balance DECIMAL(12,2) DEFAULT 1000.00;")
        
        print("Creating transactions table...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id SERIAL PRIMARY KEY,
                sender_id INTEGER REFERENCES users(id),
                receiver_id INTEGER REFERENCES users(id),
                amount DECIMAL(12,2) NOT NULL,
                type VARCHAR(20) NOT NULL, -- 'transfer', 'deposit', 'withdrawal'
                description TEXT,
                status VARCHAR(20) DEFAULT 'success',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
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
