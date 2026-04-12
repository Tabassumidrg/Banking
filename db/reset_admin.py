import os
import psycopg2
import bcrypt
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
db_url = os.environ.get('DATABASE_URL')

if not db_url:
    print("Error: DATABASE_URL not found")
    exit(1)

# New admin credentials
ADMIN_EMAIL = "admin@nidhi.bank"
ADMIN_PASSWORD = "admin123"
ADMIN_NAME = "Bank Administrator"
ADMIN_MOBILE = "9000000001"

def reset_admin():
    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cur = conn.cursor()

        # Hash the password
        hashed = bcrypt.hashpw(ADMIN_PASSWORD.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        print(f"Generated hash: {hashed}")

        # Check if admin already exists
        cur.execute("SELECT id, email, role FROM users WHERE email = %s OR role = 'admin'", (ADMIN_EMAIL,))
        existing = cur.fetchall()
        print(f"Existing admin records: {existing}")

        # Delete old admin records to avoid conflicts
        cur.execute("DELETE FROM users WHERE role = 'admin'")
        print("Cleared old admin accounts.")

        # Insert fresh admin
        cur.execute("""
            INSERT INTO users (full_name, email, mobile_number, password_hash, balance, role)
            VALUES (%s, %s, %s, %s, %s, 'admin')
            ON CONFLICT (email) DO UPDATE
            SET password_hash = EXCLUDED.password_hash,
                role = 'admin',
                full_name = EXCLUDED.full_name
            RETURNING id, email, role
        """, (ADMIN_NAME, ADMIN_EMAIL, ADMIN_MOBILE, hashed, 0.0))

        result = cur.fetchone()
        print(f"\n[SUCCESS] Admin account ready: ID={result[0]}, Email={result[1]}, Role={result[2]}")
        print(f"\n📋 Management Portal Credentials:")
        print(f"   Email:    {ADMIN_EMAIL}")
        print(f"   Password: {ADMIN_PASSWORD}")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    reset_admin()
