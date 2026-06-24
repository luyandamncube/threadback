#!/usr/bin/env python3

import json
import urllib.parse
import urllib.request
from pathlib import Path

TOKEN_FILE = Path(".tiktok_tokens.json")
VIDEO_LIST_URL = "https://open.tiktokapis.com/v2/video/list/"

tokens = json.loads(TOKEN_FILE.read_text())
access_token = tokens["access_token"]

fields = "id,title,cover_image_url,share_url,embed_link,duration,create_time"
url = VIDEO_LIST_URL + "?" + urllib.parse.urlencode({"fields": fields})

body = json.dumps({"max_count": 10}).encode("utf-8")

req = urllib.request.Request(
    url,
    data=body,
    headers={
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    },
    method="POST",
)

with urllib.request.urlopen(req, timeout=30) as resp:
    payload = json.loads(resp.read().decode("utf-8"))

print(json.dumps(payload, indent=2, sort_keys=True))
