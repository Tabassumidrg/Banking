import urllib.request
import json
import ssl

def test_login():
    url = "https://banking-backend-api.onrender.com/api/auth/signin"
    payload = {
        "email": "admin@nidhi.bank",
        "password": "Admin@1234"
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), method='POST')
    req.add_header('Content-Type', 'application/json')
    
    # Bypass SSL verification for testing if needed, though Render should be fine
    context = ssl._create_unverified_context()
    
    try:
        with urllib.request.urlopen(req, context=context) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("Login Success:")
            print(json.dumps(data, indent=2))
    except urllib.error.HTTPError as e:
        print(f"Login Failed with status {e.code}:")
        print(e.read().decode('utf-8'))
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_login()
