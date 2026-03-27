import urllib.request
import json
import os

def get_vercel_token():
    tokens_path = r'd:\saif\Banking\tokens'
    if os.path.exists(tokens_path):
        with open(tokens_path, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if 'Vercel' in line and (i + 2) < len(lines):
                    return lines[i+2].split('Value')[-1].strip()
    return None

TOKEN = get_vercel_token()
if not TOKEN:
    print("No Vercel token")
    exit(1)
    
req = urllib.request.Request('https://api.vercel.com/v6/deployments?limit=1', headers={'Authorization': f'Bearer {TOKEN}'})
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        if data['deployments']:
            dep = data['deployments'][0]
            print(f"ID: {dep['uid']}")
            print(f"State: {dep['state']}")
            print(f"URL: {dep['url']}")
            
            url2 = f"https://api.vercel.com/v11/deployments/{dep['uid']}"
            req2 = urllib.request.Request(url2, headers={'Authorization': f'Bearer {TOKEN}'})
            try:
                with urllib.request.urlopen(req2) as resp2:
                    d2 = json.loads(resp2.read().decode('utf-8'))
                    if 'error' in d2:
                        print('Error:', d2['error'])
            except urllib.error.HTTPError as e:
                print('HTTPError checking specific deployment:', e.read().decode())
                
            if dep['state'] == 'ERROR':
                print("Fetching build logs...")
                url3 = f"https://api.vercel.com/v2/deployments/{dep['uid']}/events"
                req3 = urllib.request.Request(url3, headers={'Authorization': f'Bearer {TOKEN}'})
                try:
                    with urllib.request.urlopen(req3) as resp3:
                        for line in resp3:
                            if not line.strip(): continue
                            try:
                                event = json.loads(line.decode('utf-8'))
                                if 'payload' in event and 'text' in event['payload']:
                                    print(event['payload']['text'])
                            except: pass
                except Exception as e:
                    print("Error fetching logs:", e)
        else:
            print('No deployments found')
except Exception as e:
    print('Exception:', e)
