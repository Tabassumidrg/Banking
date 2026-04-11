import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load .env from the db folder
dotenv_path = os.path.join(os.getcwd(), 'db', '.env')
load_dotenv(dotenv_path=dotenv_path)

db_url = os.environ.get("DATABASE_URL")

def check_admin():
    if not db_url:
        print("DATABASE_URL not found in .env")
        return

    try:
        print(f"Connecting to: {db_url[:20]}...")
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("SELECT id, full_name, email, role FROM users WHERE role = 'admin' OR email LIKE '%%nidhi%%'")
        users = cur.fetchall()
        
        if not users:
            print("No admin users or 'nidhi' users found.")
        else:
            print("Found users:")
            for u in users:
                print(f" - ID: {u['id']}, Name: {u['full_name']}, Email: {u['email']}, Role: {u['role']}")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_admin()
