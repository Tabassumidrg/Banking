import urllib.request
import json

def test_login():
    url = "https://banking-backend-api.onrender.com/api/auth/signin"
    payload = {
        "email": "admin@nidhi.bank",
        "password": "admin123"
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), method='POST')
    req.add_header('Content-Type', 'application/json')
    
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("Login Success:")
            print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Login Failed: {e}")

if __name__ == "__main__":
    test_login()
