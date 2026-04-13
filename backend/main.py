import os
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import bcrypt
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Try to load local .env if it exists
load_dotenv(dotenv_path="../db/.env")
db_url = os.environ.get("DATABASE_URL")

app = FastAPI(title="Nidhi Bank API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Note: passlib.context.CryptContext was causing a 72-byte ValueError with modern bcrypt versions
# We now use the bcrypt library directly.

class UserSignup(BaseModel):
    full_name: str
    email: str
    mobile_number: str
    password: str
    role: str = "user"

class UserLogin(BaseModel):
    email: str
    password: str

class TransferRequest(BaseModel):
    sender_id: int
    receiver_email: str
    amount: float
    description: str = "Transfer"

class PasswordChangeRequest(BaseModel):
    user_id: int
    current_password: str
    new_password: str

class TwoFactorToggleRequest(BaseModel):
    user_id: int
    enabled: bool

class UserAdminCreate(BaseModel):
    full_name: str
    email: str
    mobile_number: str
    password: str
    balance: float = 0.0
    role: str = "user"

class UserUpdate(BaseModel):
    full_name: str
    email: str
    mobile_number: str
    balance: float
    role: str = "user"

class KYCUpdate(BaseModel):
    user_id: int
    status: str
    notes: str = ""

class ServiceRequestCreate(BaseModel):
    user_id: int
    type: str
    details: str

class ServiceRequestUpdate(BaseModel):
    status: str

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Nidhi Bank Backend is running - Version: 1.0.2-Verified"}

@app.get("/api/debug/db")
def debug_db():
    url = os.environ.get("DATABASE_URL", "NOT_SET")
    return {"host_prefix": url.split("@")[-1][:20] if "@" in url else "No @ found"}

def log_event(user_id: int, action: str, details: str, ip: str = None):
    if not db_url: return
    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO audit_logs (user_id, action, details, ip_address) VALUES (%s, %s, %s, %s)",
            (user_id, action, details, ip)
        )
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Logging error: {e}")

@app.post("/api/auth/signup")
def signup(user: UserSignup):
    if not db_url:
        raise HTTPException(status_code=500, detail="Database isn't configured")
        
    try:
        conn = psycopg2.connect(db_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    try:
        conn.autocommit = True
        cur = conn.cursor(cursor_factory=RealDictCursor)
        # Check if exists
        cur.execute("SELECT id FROM users WHERE email = %s OR mobile_number = %s", (user.email, user.mobile_number))
        if cur.fetchone():
            raise HTTPException(status_code=400, detail="Email or Mobile Number already registered")
            
        # Salt is generated automatically in hashpw
        password_bytes = user.password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_pwd = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
        cur.execute(
            "INSERT INTO users (full_name, email, mobile_number, password_hash, role) VALUES (%s, %s, %s, %s, %s) RETURNING id, full_name, email, mobile_number, role",
            (user.full_name, user.email, user.mobile_number, hashed_pwd, user.role)
        )
        new_user = cur.fetchone()
        log_event(new_user["id"], "SIGNUP", f"New account created: {new_user['email']}")
        return {"message": "Account created successfully!", "user": new_user}
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.post("/api/auth/signin")
def signin(user: UserLogin):
    if not db_url:
        raise HTTPException(status_code=500, detail="Database isn't configured")
        
    try:
        conn = psycopg2.connect(db_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT id, full_name, email, password_hash, role FROM users WHERE email = %s", (user.email,))
        db_user = cur.fetchone()
        
        if not db_user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
            
        password_bytes = user.password.encode('utf-8')
        db_hash_bytes = db_user["password_hash"].encode('utf-8')
        
        if not bcrypt.checkpw(password_bytes, db_hash_bytes):
            log_event(db_user["id"], "LOGIN_FAILED", f"Failed login attempt for {user.email}")
            raise HTTPException(status_code=401, detail="Invalid email or password")
            
        log_event(db_user["id"], "LOGIN_SUCCESS", f"User logged in: {user.email}")
        return {"message": "Login successful", "user": {"id": db_user["id"], "full_name": db_user["full_name"], "email": db_user["email"], "role": db_user["role"]}}
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.get("/api/dashboard/summary/{user_id}")
def get_summary(user_id: int):
    if not db_url:
        raise HTTPException(status_code=500, detail="Database isn't configured")
    
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get balance
        cur.execute("SELECT balance, email FROM users WHERE id = %s", (user_id,))
        user_info = cur.fetchone()
        if not user_info:
            raise HTTPException(status_code=404, detail="User not found")
            
        # Get last 5 transactions
        cur.execute("""
            SELECT t.*, 
                   u_s.email as sender_email, 
                   u_r.email as receiver_email
            FROM transactions t
            LEFT JOIN users u_s ON t.sender_id = u_s.id
            LEFT JOIN users u_r ON t.receiver_id = u_r.id
            WHERE t.sender_id = %s OR t.receiver_id = %s
            ORDER BY t.created_at DESC
            LIMIT 5
        """, (user_id, user_id))
        transactions = cur.fetchall()
        
        return {
            "balance": float(user_info["balance"]),
            "email": user_info["email"],
            "transactions": transactions
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.get("/api/admin/branch-stats")
def get_branch_stats():
    if not db_url:
        raise HTTPException(status_code=500, detail="Database isn't configured")
    
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # 1. Total User Count
        cur.execute("SELECT COUNT(*) as total_users FROM users")
        total_users = cur.fetchone()["total_users"]
        
        # 2. Total Branch Balance
        cur.execute("SELECT SUM(balance) as total_balance FROM users")
        total_balance = float(cur.fetchone()["total_balance"] or 0)
        
        # 3. Total Transactions Today
        cur.execute("SELECT COUNT(*) as transactions_today FROM transactions WHERE DATE(created_at) = CURRENT_DATE")
        transactions_today = cur.fetchone()["transactions_today"]
        
        # 4. Recent Global Transactions (last 5)
        cur.execute("""
            SELECT t.*, u_s.full_name as sender_name, u_r.full_name as receiver_name 
            FROM transactions t
            LEFT JOIN users u_s ON t.sender_id = u_s.id
            LEFT JOIN users u_r ON t.receiver_id = u_r.id
            ORDER BY t.created_at DESC LIMIT 10
        """)
        recent_global_transactions = cur.fetchall()

        # 5. High-Value Alerts (Transactions > 1,00,000)
        cur.execute("""
            SELECT t.*, u_s.full_name as sender_name, u_r.full_name as receiver_name 
            FROM transactions t
            LEFT JOIN users u_s ON t.sender_id = u_s.id
            LEFT JOIN users u_r ON t.receiver_id = u_r.id
            WHERE t.amount >= 100000
            ORDER BY t.created_at DESC LIMIT 5
        """)
        high_value_alerts = cur.fetchall()

        # 6. Branch Growth (Users per day for last 7 days)
        cur.execute("""
            SELECT DATE(created_at) as date, COUNT(*) as count
            FROM users
            WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'
            GROUP BY DATE(created_at)
            ORDER BY DATE(created_at) ASC
        """)
        growth_raw = cur.fetchall()
        
        return {
            "total_users": total_users,
            "total_balance": total_balance,
            "transactions_today": transactions_today,
            "recent_transactions": recent_global_transactions,
            "high_value_alerts": high_value_alerts,
            "growth_trend": growth_raw
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.get("/api/admin/security-stats")
def get_security_stats():
    if not db_url:
        raise HTTPException(status_code=500, detail="Database isn't configured")
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # 1. 2FA Adoption Rate
        cur.execute("SELECT COUNT(*) as total FROM users")
        total_users = cur.fetchone()["total"]
        cur.execute("SELECT COUNT(*) as enabled FROM users WHERE is_2fa_enabled = TRUE")
        enabled_users = cur.fetchone()["enabled"]
        adoption_rate = (enabled_users / total_users * 100) if total_users > 0 else 0
        
        # 2. Unusual Admin Activity (last 24h)
        cur.execute("""
            SELECT COUNT(*) as count FROM audit_logs 
            WHERE action LIKE 'ADMIN_%' AND created_at >= CURRENT_TIMESTAMP - INTERVAL '24 hours'
        """)
        admin_activity = cur.fetchone()["count"]
        
        # 3. Recent Admin Logins (for session oversight)
        cur.execute("""
            SELECT a.created_at, u.full_name as user_name, u.email as user_email, a.ip_address
            FROM audit_logs a
            JOIN users u ON a.user_id = u.id
            WHERE u.role = 'admin' AND a.action = 'LOGIN_SUCCESS'
            ORDER BY a.created_at DESC LIMIT 5
        """)
        recent_admin_logins = cur.fetchall()
        
        # 4. Calculate a Mock Security Score (0-100)
        # Factor 1: 2FA adoption (40%)
        # Factor 2: Admin activity density (40%) - lower is safer for some actions
        # Factor 3: High value alerts (20%) - derived from transactions
        cur.execute("SELECT COUNT(*) as count FROM transactions WHERE amount >= 100000 AND created_at >= CURRENT_TIMESTAMP - INTERVAL '7 days'")
        high_value_week = cur.fetchone()["count"]
        
        score = (adoption_rate * 0.4) + (max(0, 100 - admin_activity * 5) * 0.4) + (max(0, 100 - high_value_week * 10) * 0.2)
        score = min(100, max(0, score))

        return {
            "tfa_adoption_rate": round(adoption_rate, 1),
            "recent_admin_activity_count": admin_activity,
            "recent_admin_logins": recent_admin_logins,
            "branch_security_score": round(score, 1)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.get("/api/admin/audit-logs")
def get_audit_logs():
    if not db_url:
        raise HTTPException(status_code=500, detail="Database isn't configured")
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT a.*, u.email as user_email, u.full_name as user_name
            FROM audit_logs a
            LEFT JOIN users u ON a.user_id = u.id
            ORDER BY a.created_at DESC LIMIT 50
        """)
        logs = cur.fetchall()
        return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

# --- New Operations Hub Endpoints ---

@app.get("/api/admin/kyc/pending")
def get_pending_kyc():
    if not db_url:
        raise HTTPException(status_code=500, detail="Database isn't configured")
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT id, full_name, email, mobile_number, kyc_status, created_at FROM users WHERE kyc_status = 'pending' AND role != 'admin' ORDER BY created_at DESC")
        users = cur.fetchall()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.put("/api/admin/kyc/update")
def update_kyc_status(req: KYCUpdate):
    if not db_url:
        raise HTTPException(status_code=500, detail="Database isn't configured")
    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            "UPDATE users SET kyc_status = %s, kyc_notes = %s WHERE id = %s RETURNING id, email, kyc_status",
            (req.status, req.notes, req.user_id)
        )
        updated = cur.fetchone()
        if not updated:
            raise HTTPException(status_code=404, detail="User not found")
        log_event(None, "ADMIN_KYC_UPDATE", f"Admin updated KYC for user ID: {req.user_id} to {req.status}")
        return {"message": f"KYC status updated to {req.status}", "user": updated}
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.get("/api/admin/service-requests")
def list_all_service_requests():
    if not db_url:
        raise HTTPException(status_code=500, detail="Database isn't configured")
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT sr.*, u.full_name as user_name, u.email as user_email
            FROM service_requests sr
            JOIN users u ON sr.user_id = u.id
            ORDER BY sr.created_at DESC
        """)
        requests = cur.fetchall()
        return requests
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.patch("/api/admin/service-requests/{req_id}")
def update_service_request_status(req_id: int, req: ServiceRequestUpdate):
    if not db_url:
        raise HTTPException(status_code=500, detail="Database isn't configured")
    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            "UPDATE service_requests SET status = %s WHERE id = %s RETURNING id, status",
            (req.status, req_id)
        )
        updated = cur.fetchone()
        if not updated:
            raise HTTPException(status_code=404, detail="Request not found")
        log_event(None, "ADMIN_SERVICE_UPDATE", f"Admin updated service request {req_id} to {req.status}")
        return {"message": "Service request status updated", "request": updated}
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.post("/api/user/service-requests")
def create_service_request(req: ServiceRequestCreate):
    if not db_url:
        raise HTTPException(status_code=500, detail="Database isn't configured")
    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            "INSERT INTO service_requests (user_id, type, details) VALUES (%s, %s, %s) RETURNING id, type, status",
            (req.user_id, req.type, req.details)
        )
        new_req = cur.fetchone()
        log_event(req.user_id, "SERVICE_REQUEST_CREATED", f"User created {req.type} request")
        return {"message": "Service request submitted successfully", "request": new_req}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.get("/api/users")
def list_users():
    if not db_url:
        raise HTTPException(status_code=500, detail="Database isn't configured")
    
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("SELECT id, full_name, email, mobile_number, balance, role, created_at FROM users ORDER BY created_at DESC")
        users = cur.fetchall()
        
        # Convert balance to float for JSON serialization
        for u in users:
            u["balance"] = float(u["balance"])
            
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.post("/api/users")
def admin_create_user(user: UserAdminCreate):
    if not db_url:
        raise HTTPException(status_code=500, detail="Database isn't configured")
        
    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Check if exists
        cur.execute("SELECT id FROM users WHERE email = %s OR mobile_number = %s", (user.email, user.mobile_number))
        if cur.fetchone():
            raise HTTPException(status_code=400, detail="Email or Mobile Number already registered")
            
        password_bytes = user.password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_pwd = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
        
        cur.execute(
            "INSERT INTO users (full_name, email, mobile_number, password_hash, balance, role) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id, full_name, email, mobile_number, balance, role",
            (user.full_name, user.email, user.mobile_number, hashed_pwd, user.balance, user.role)
        )
        new_user = cur.fetchone()
        new_user["balance"] = float(new_user["balance"])
        log_event(None, "ADMIN_CREATE_USER", f"Admin created user: {new_user['email']}")
        return {"message": "User created successfully!", "user": new_user}
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.put("/api/users/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    if not db_url:
        raise HTTPException(status_code=500, detail="Database isn't configured")
        
    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute(
            "UPDATE users SET full_name = %s, email = %s, mobile_number = %s, balance = %s, role = %s WHERE id = %s RETURNING id, full_name, email, mobile_number, balance, role",
            (user.full_name, user.email, user.mobile_number, user.balance, user.role, user_id)
        )
        updated_user = cur.fetchone()
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
            
        updated_user["balance"] = float(updated_user["balance"])
        log_event(None, "ADMIN_UPDATE_USER", f"Admin updated user ID: {user_id} ({updated_user['email']})")
        return {"message": "User updated successfully!", "user": updated_user}
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.delete("/api/users/{user_id}")
def delete_user(user_id: int):
    if not db_url:
        raise HTTPException(status_code=500, detail="Database isn't configured")
        
    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Also delete transactions associated with this user
        cur.execute("DELETE FROM transactions WHERE sender_id = %s OR receiver_id = %s", (user_id, user_id))
        cur.execute("DELETE FROM users WHERE id = %s RETURNING id", (user_id,))
        deleted = cur.fetchone()
        
        if not deleted:
            raise HTTPException(status_code=404, detail="User not found")
            
        log_event(None, "ADMIN_DELETE_USER", f"Admin deleted user ID: {user_id}")
        return {"message": "User and associated transactions deleted successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.post("/api/transactions/transfer")
def transfer_funds(req: TransferRequest):
    if not db_url:
        raise HTTPException(status_code=500, detail="Database isn't configured")
    
    if req.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
        
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # 1. Check sender balance
        cur.execute("SELECT balance FROM users WHERE id = %s", (req.sender_id,))
        sender = cur.fetchone()
        if not sender:
            raise HTTPException(status_code=404, detail="Sender not found")
        
        if float(sender["balance"]) < req.amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")
            
        # 2. Check receiver exists
        cur.execute("SELECT id FROM users WHERE email = %s", (req.receiver_email,))
        receiver = cur.fetchone()
        if not receiver:
            raise HTTPException(status_code=404, detail="Receiver email not registered")
            
        if receiver["id"] == req.sender_id:
            raise HTTPException(status_code=400, detail="Cannot transfer to yourself")

        # Daily Limits Check (2.5 Lakhs Sent/Received per day)
        cur.execute("""
            SELECT COALESCE(SUM(amount), 0) as daily_sent
            FROM transactions
            WHERE sender_id = %s AND DATE(created_at) = CURRENT_DATE
        """, (req.sender_id,))
        daily_sent = float(cur.fetchone()["daily_sent"])
        if daily_sent + req.amount > 250000:
            raise HTTPException(status_code=400, detail="Daily sending limit of ₹2,50,000 exceeded. Please wait until tomorrow.")
            
        cur.execute("""
            SELECT COALESCE(SUM(amount), 0) as daily_received
            FROM transactions
            WHERE receiver_id = %s AND DATE(created_at) = CURRENT_DATE
        """, (receiver["id"],))
        daily_received = float(cur.fetchone()["daily_received"])
        if daily_received + req.amount > 250000:
            raise HTTPException(status_code=400, detail="Receiver's daily receiving limit of ₹2,50,000 exceeded. Please wait until tomorrow.")

        # 3. Perform transfer via SQL Transaction
        cur.execute("BEGIN;")
        try:
            # Deduct from sender
            cur.execute("UPDATE users SET balance = balance - %s WHERE id = %s", (req.amount, req.sender_id))
            # Add to receiver
            cur.execute("UPDATE users SET balance = balance + %s WHERE id = %s", (req.amount, receiver["id"]))
            # Log transaction
            cur.execute("""
                INSERT INTO transactions (sender_id, receiver_id, amount, type, description)
                VALUES (%s, %s, %s, 'transfer', %s)
            """, (req.sender_id, receiver["id"], req.amount, req.description))
            cur.execute("COMMIT;")
        except Exception as e:
            cur.execute("ROLLBACK;")
            raise e
            
        log_event(req.sender_id, "TRANSFER_SENT", f"Transfer of ₹{req.amount} to {req.receiver_email}")
        return {"message": "Transfer successful!"}
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.post("/api/auth/password/update")
def update_password(req: PasswordChangeRequest):
    if not db_url:
        raise HTTPException(status_code=500, detail="Database isn't configured")
        
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # 1. Fetch user to verify current password
        cur.execute("SELECT password_hash FROM users WHERE id = %s", (req.user_id,))
        user = cur.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        # 2. Verify current password
        if not bcrypt.checkpw(req.current_password.encode('utf-8'), user["password_hash"].encode('utf-8')):
            raise HTTPException(status_code=401, detail="Incorrect current password")
            
        # 3. Hash and update new password
        salt = bcrypt.gensalt()
        new_hashed_password = bcrypt.hashpw(req.new_password.encode('utf-8'), salt).decode('utf-8')
        
        cur.execute("UPDATE users SET password_hash = %s WHERE id = %s", (new_hashed_password, req.user_id))
        conn.commit()
        
        return {"message": "Password updated successfully!"}
        
@app.post("/api/auth/2fa/toggle")
def toggle_2fa(req: TwoFactorToggleRequest):
    if not db_url:
        raise HTTPException(status_code=500, detail="Database isn't configured")
    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("UPDATE users SET is_2fa_enabled = %s WHERE id = %s RETURNING email", (req.enabled, req.user_id))
        res = cur.fetchone()
        if not res:
            raise HTTPException(status_code=404, detail="User not found")
        
        status = "ENABLED" if req.enabled else "DISABLED"
        log_event(req.user_id, "2FA_TOGGLE", f"Two-Factor Authentication {status} for {res[0]}")
        return {"message": f"2FA {status} successfully", "enabled": req.enabled}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
