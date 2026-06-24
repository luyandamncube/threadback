# vercel-callback

Tiny Vercel project for receiving OAuth callback redirects while testing TikTok Login Kit.

The callback endpoint displays the OAuth `code`, `state`, and granted scopes in the browser. You can then copy the `code` into a local token exchange script.

## Endpoints

After deployment, your project will have:

```text
https://YOUR-VERCEL-PROJECT.vercel.app/api/callback
```

Register that exact URL as the TikTok Login Kit redirect URI.

## Deploy

```bash
npm i -g vercel
vercel login
vercel --prod
```

Use the production deployment URL from Vercel, then append:

```text
/api/callback
```

Example:

```text
https://vercel-callback-yourname.vercel.app/api/callback
```

## Local TikTok env

Copy the example file:

```bash
cp .env.example .env.tiktok
```

Edit `.env.tiktok` with your TikTok app credentials and deployed callback URL:

```bash
source .env.tiktok
```

## Generate TikTok auth URL

```bash
./scripts/tiktok_make_auth_url.py
```

Open the printed URL in your browser. TikTok should redirect to the Vercel callback page and show a `code`.

## Exchange code for tokens

```bash
./scripts/tiktok_exchange_code.py 'PASTE_CODE_FROM_CALLBACK_PAGE'
```

The token response is saved to:

```text
.tiktok_tokens.json
```

This file is ignored by git.

## Notes

- Do not commit `.env.tiktok`, `.env`, or `.tiktok_tokens.json`.
- The TikTok redirect URI must match exactly between TikTok Developer settings and `TIKTOK_REDIRECT_URI`.
- This project is intentionally minimal and meant for developer testing, not production user auth.
