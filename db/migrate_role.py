import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(dotenv_path='d:\\saif\\Banking\\db\\.env')
db_url = os.environ.get('DATABASE_URL')

def migrate():
    print("Connecting to database...")
    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cur = conn.cursor()
        
        print("Adding 'role' column to 'users' table...")
        try:
            cur.execute("ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user';")
            print("Column added successfully.")
        except Exception as e:
            if "already exists" in str(e):
                print("Column 'role' already exists.")
            else:
                raise e
        
        print("Setting 'nidhi.sharma@nidhi.bank' as admin...")
        cur.execute("UPDATE users SET role = 'admin' WHERE email = %s", ('nidhi.sharma@nidhi.bank',))
        
        # Also check if there's any user at all, if not, maybe we should know
        cur.execute("SELECT email, role FROM users WHERE role = 'admin'")
        admins = cur.fetchall()
        print(f"Current admins: {admins}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    migrate()
