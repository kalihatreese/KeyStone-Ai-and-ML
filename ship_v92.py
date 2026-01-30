import json, requests, os

# Load credentials from your environment
auth_email = os.getenv('CF_EMAIL')
auth_key = os.getenv('CF_KEY')
account_id = os.getenv('CF_ACCOUNT')
script_name = "keystone-v92-resurrection"

# Read the local manifest
with open('index.html', 'r') as f:
    html_content = f.read()

# Build the Worker Script Body
# This embeds your HTML directly into the response logic
worker_script = f"""
addEventListener('fetch', event => {{
  event.respondWith(new Response({json.dumps(html_content)}, {{
    headers: {{ 'Content-Type': 'text/html;charset=UTF-8' }}
  }}))
}})
"""

# Push to the Cloudflare Edge
url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/workers/scripts/{script_name}"
headers = {
    "X-Auth-Email": auth_email,
    "X-Auth-Key": auth_key,
    "Content-Type": "application/javascript"
}

print(f"[V] SENTINEL: Shipping V92 Manifest to {script_name}...")
response = requests.put(url, headers=headers, data=worker_script)
print(response.json())
