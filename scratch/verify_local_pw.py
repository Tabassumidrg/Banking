import os
import psycopg2
import bcrypt
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

dotenv_path = os.path.join(os.getcwd(), 'db', '.env')
load_dotenv(dotenv_path=dotenv_path)

db_url = os.environ.get("DATABASE_URL")

def verify_local_password():
    email = "admin@nidhi.bank"
    password = "Admin@1234"
    
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("SELECT password_hash FROM users WHERE email = %s", (email,))
        row = cur.fetchone()
        
        if not row:
            print(f"User {email} not found in database.")
            return
            
        hashed = row['password_hash']
        if bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8')):
            print(f"✅ Password verified locally for {email}!")
        else:
            print(f"❌ Password verification FAILED locally for {email}.")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_local_password()
