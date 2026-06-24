#!/usr/bin/env python3

import json
import urllib.parse
import urllib.request
from pathlib import Path

TOKEN_FILE = Path(".tiktok_tokens.json")
USER_INFO_URL = "https://open.tiktokapis.com/v2/user/info/"

tokens = json.loads(TOKEN_FILE.read_text())
access_token = tokens["access_token"]

fields = "open_id,union_id,avatar_url,display_name"
url = USER_INFO_URL + "?" + urllib.parse.urlencode({"fields": fields})

req = urllib.request.Request(
    url,
    headers={"Authorization": f"Bearer {access_token}"},
    method="GET",
)

with urllib.request.urlopen(req, timeout=30) as resp:
    payload = json.loads(resp.read().decode("utf-8"))

print(json.dumps(payload, indent=2, sort_keys=True))
