#!/usr/bin/env python3
# Generate stock images via Cloudflare Workers AI FLUX.1-schnell (free tier).
# Usage: python3 fluxgen.py <prompt> <out.jpg>   (needs CF_AI_TOKEN + CF_ACCOUNT_ID env)
import json, os, sys, base64, urllib.request
acct = os.environ.get("CF_ACCOUNT_ID", "aad16187ac08795a47221bc8e3e62ebd")
token = os.environ["CF_AI_TOKEN"]
prompt, out = sys.argv[1], sys.argv[2]
req = urllib.request.Request(
    f"https://api.cloudflare.com/client/v4/accounts/{acct}/ai/run/@cf/black-forest-labs/flux-1-schnell",
    data=json.dumps({"prompt": prompt, "steps": 4}).encode(),
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
resp = json.load(urllib.request.urlopen(req, timeout=120))
img = resp["result"]["image"]
data = base64.b64decode(img) if isinstance(img, str) else img
open(out, "wb").write(data)
print(out, len(data))
