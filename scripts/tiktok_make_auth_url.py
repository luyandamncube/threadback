#!/usr/bin/env python3

import os
import secrets
import urllib.parse

AUTH_URL = "https://www.tiktok.com/v2/auth/authorize/"

def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise SystemExit(f"Missing env var: {name}")
    return value

def main():
    client_key = require_env("TIKTOK_CLIENT_KEY")
    redirect_uri = require_env("TIKTOK_REDIRECT_URI")
    scopes = os.getenv("TIKTOK_SCOPES", "user.info.basic,video.list")
    state = secrets.token_urlsafe(32)

    params = {
        "client_key": client_key,
        "response_type": "code",
        "scope": scopes,
        "redirect_uri": redirect_uri,
        "state": state,
    }

    url = AUTH_URL + "?" + urllib.parse.urlencode(params)

    print("State:")
    print(state)
    print()
    print("Open this URL:")
    print(url)

if __name__ == "__main__":
    main()
