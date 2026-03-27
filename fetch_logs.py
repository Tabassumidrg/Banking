import urllib.request, json, os

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
req = urllib.request.Request('https://api.vercel.com/v6/deployments?limit=1', headers={'Authorization': f'Bearer {TOKEN}'})
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        dep = data['deployments'][0]
        url3 = f"https://api.vercel.com/v2/deployments/{dep['uid']}/events"
        req3 = urllib.request.Request(url3, headers={'Authorization': f'Bearer {TOKEN}'})
        with open(r'd:\saif\Banking\vercel_logs_utf8.txt', 'w', encoding='utf-8') as out:
            with urllib.request.urlopen(req3) as resp3:
                for line in resp3:
                    if not line.strip(): continue
                    try:
                        event = json.loads(line.decode('utf-8'))
                        if 'payload' in event and 'text' in event['payload']:
                            out.write(event['payload']['text'] + '\n')
                    except Exception as e: pass
except Exception as e:
    print(e)
