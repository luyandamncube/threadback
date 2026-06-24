#!/usr/bin/env python3

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"
TOKEN_FILE = Path(os.getenv("TIKTOK_TOKEN_FILE", ".tiktok_tokens.json"))

def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise SystemExit(f"Missing env var: {name}")
    return value

def post_form(url: str, data: dict) -> dict:
    body = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {e.code}\n{raw}") from e

def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: ./scripts/tiktok_exchange_code.py '<code-from-callback-page>'")

    code = sys.argv[1]

    payload = post_form(
        TOKEN_URL,
        {
            "client_key": require_env("TIKTOK_CLIENT_KEY"),
            "client_secret": require_env("TIKTOK_CLIENT_SECRET"),
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": require_env("TIKTOK_REDIRECT_URI"),
        },
    )

    payload["saved_at_epoch"] = int(time.time())

    TOKEN_FILE.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.chmod(TOKEN_FILE, 0o600)

    print("Token exchange response:")
    print(json.dumps(payload, indent=2, sort_keys=True))
    print(f"\nSaved: {TOKEN_FILE}")

if __name__ == "__main__":
    main()
