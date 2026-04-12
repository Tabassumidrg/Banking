import urllib.request
import json
import uuid

def test_signup_login():
    email = f"test_{uuid.uuid4().hex[:6]}@example.com"
    password = "TestPassword@123"
    
    # 1. Signup
    signup_url = "https://banking-backend-api.onrender.com/api/auth/signup"
    signup_payload = {
        "full_name": "Test User",
        "email": email,
        "mobile_number": "9" + "".join([str(uuid.uuid4().int % 10) for _ in range(9)]),
        "password": password
    }
    
    print(f"Attempting signup for {email}...")
    req = urllib.request.Request(signup_url, data=json.dumps(signup_payload).encode('utf-8'), method='POST')
    req.add_header('Content-Type', 'application/json')
    
    try:
        with urllib.request.urlopen(req) as resp:
            print("Signup Success!")
    except Exception as e:
        print(f"Signup Failed: {e}")
        return

    # 2. Login
    signin_url = "https://banking-backend-api.onrender.com/api/auth/signin"
    signin_payload = {
        "email": email,
        "password": password
    }
    
    print(f"Attempting signin for {email}...")
    req = urllib.request.Request(signin_url, data=json.dumps(signin_payload).encode('utf-8'), method='POST')
    req.add_header('Content-Type', 'application/json')
    
    try:
        with urllib.request.urlopen(req) as resp:
            print("Signin Success!")
            data = json.loads(resp.read().decode('utf-8'))
            print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Signin Failed: {e}")

if __name__ == "__main__":
    test_signup_login()
