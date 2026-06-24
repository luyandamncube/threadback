# Threadback

A tiny OAuth callback postbox for dev flows.

Threadback is a small Vercel-hosted utility for testing OAuth redirect/callback flows with APIs that require a public HTTPS redirect URI.

It is intentionally minimal:

* Vercel hosts a public HTTPS callback endpoint.
* The callback stores the returned OAuth `code` by `state` for a short TTL.
* Local scripts poll `/api/code?state=...` and exchange the returned code for tokens.
* Secrets and access/refresh tokens stay local and are not stored by Vercel.

## Project structure

```text
threadback/
├── api/
│   ├── callback.js              # OAuth callback receiver; stores code by state
│   ├── code.js                  # Local polling endpoint; returns code by state
│   └── index.js                 # Small API landing page
├── public/
│   ├── index.html               # Public landing page
│   ├── privacy.html             # Placeholder privacy policy
│   └── terms.html               # Placeholder terms page
├── scripts/
│   ├── tiktok_make_auth_url.py  # Generates TikTok Login Kit auth URL
│   └── tiktok_exchange_code.py  # Exchanges auth code for tokens
├── index.html                   # Repo-visible landing page copy
├── privacy.html                 # Repo-visible privacy page copy
├── terms.html                   # Repo-visible terms page copy
├── .env.example
├── .gitignore
├── package.json
├── vercel.json
└── README.md
```

## What Threadback is for

Use this when an OAuth provider needs a public HTTPS redirect URI, but you still want to run the actual token exchange and API tests locally.

Example flow:

```text
OAuth provider
→ redirects to Threadback callback URL
→ Threadback stores code by state in short-lived KV storage
→ local script polls /api/code?state=...
→ local script exchanges code for tokens
→ local API testing continues
```

## What Threadback is not

Threadback is not a production auth system.

It does not:

* Persist users.
* Store OAuth codes permanently. Codes are stored only temporarily for local polling.
* Store access tokens.
* Validate state server-side.
* Manage sessions.
* Refresh tokens automatically.
* Provide a production-grade consent/login experience.

Use it as a developer utility only.

## Deploy to Vercel

Install the Vercel CLI:

```bash
npm i -g vercel
```

Log in:

```bash
vercel login
```

Deploy from the project root:

```bash
vercel --prod
```

When prompted, typical answers are:

```text
Project? Create new project
Name? threadback
Code directory? ./
Customize settings? no
Customize advanced settings? no
```

After deployment, Vercel should give you a production URL and an alias.

Example:

```text
https://threadback.vercel.app
```

Your OAuth callback URL is:

```text
https://threadback.vercel.app/api/callback
```

The local polling URL is:

```text
https://threadback.vercel.app/api/code
```

## Required Vercel environment variables

Threadback needs a Vercel KV/Redis-compatible store for the short-lived OAuth code postbox. Set these in the Vercel project environment:

```text
KV_REST_API_URL=<your Upstash/Vercel KV REST URL>
KV_REST_API_TOKEN=<your Upstash/Vercel KV REST token>
```

For Upstash Redis, these usually map to:

```text
KV_REST_API_URL=UPSTASH_REDIS_REST_URL
KV_REST_API_TOKEN=UPSTASH_REDIS_REST_TOKEN
```

After adding or changing env vars, redeploy:

```bash
vercel --prod
```

## Verify the API routes

Check the code endpoint returns JSON before a real OAuth run:

```bash
curl 'https://threadback.vercel.app/api/code?state=test&consume=true'
```

Expected when no code is stored:

```json
{"ok":false,"error":"not_found"}
```

## Verify the callback page

Open this in your browser:

```text
https://threadback.vercel.app/api/callback?code=test123&state=teststate&scopes=user.info.basic,video.list
```

You should see a page showing:

```text
code
state
scopes
```

## Public service pages

Threadback includes placeholder pages that can be used when a developer portal asks for service URLs:

```text
https://threadback.vercel.app/
https://threadback.vercel.app/privacy.html
https://threadback.vercel.app/terms.html
```

These are placeholder developer-testing pages. Replace them with reviewed real pages before using this with production users.

## TikTok Login Kit setup

In TikTok Developer settings, register the callback URL exactly:

```text
https://threadback.vercel.app/api/callback
```

Also use the public pages where required:

```text
App / Web URL:
https://threadback.vercel.app/

Privacy Policy:
https://threadback.vercel.app/privacy.html

Terms of Service:
https://threadback.vercel.app/terms.html
```

The redirect URI must match exactly between TikTok Developer settings and your local env.

These are different values:

```text
https://threadback.vercel.app/api/callback
https://threadback.vercel.app/api/callback/
```

Use one version consistently. The current recommended value is:

```text
https://threadback.vercel.app/api/callback
```

## Local environment

Copy the example env file:

```bash
cp .env.example .env.tiktok
```

Edit `.env.tiktok`:

```bash
export TIKTOK_CLIENT_KEY="your_client_key"
export TIKTOK_CLIENT_SECRET="your_client_secret"
export TIKTOK_REDIRECT_URI="https://threadback.vercel.app/api/callback"
export TIKTOK_SCOPES="user.info.basic,video.list"
```

Load it:

```bash
source .env.tiktok
```

Do not commit `.env.tiktok`.

## Generate TikTok auth URL

Run:

```bash
./scripts/tiktok_make_auth_url.py
```

The script prints:

```text
State:
...

Open this URL:
https://www.tiktok.com/v2/auth/authorize/?...
```

Open the printed URL in your browser.

After approving the TikTok login, TikTok redirects to Threadback. Threadback stores the returned `code` by `state` for a short TTL and shows a success page containing the `state`, `scopes`, and expiry window. It no longer needs to display the code for the automated flow.

## Retrieve the code from the postbox

Local scripts or Stitchly can poll the code endpoint with the generated `state`:

```bash
curl 'https://threadback.vercel.app/api/code?state=STATE_FROM_AUTH_URL&consume=true'
```

When no code has arrived yet, the expected response is:

```json
{"ok":false,"error":"not_found"}
```

When the callback has stored a code, the expected response is:

```json
{
  "ok": true,
  "code": "...",
  "state": "...",
  "scopes": "user.info.basic,video.list",
  "receivedAt": "..."
}
```

By default `consume=true` deletes the code after it is read. Use `consume=false` only while debugging.

## Exchange the code for tokens

The recommended flow is for a local script or Stitchly pipeline to exchange the code after reading `/api/code`. Token exchange still happens locally so TikTok client secrets and access/refresh tokens do not live in Threadback.

Manual fallback:

```bash
./scripts/tiktok_exchange_code.py 'PASTE_CODE_FROM_API_CODE_RESPONSE'
```

If successful, the script prints the token response and saves it locally:

```text
.tiktok_tokens.json
```

This file is ignored by git.

Expected token response fields include:

```text
access_token
refresh_token
open_id
scope
expires_in
refresh_expires_in
token_type
saved_at_epoch
```

Treat these values as sensitive:

```text
access_token
refresh_token
open_id
```

## Stitchly pipeline usage

For Stitchly v2, Threadback acts as a tiny OAuth postbox:

```text
Stitchly Make Auth URL node
→ browser approval at TikTok
→ TikTok redirects to /api/callback
→ Threadback stores code by state
→ Stitchly Wait And Exchange Auth node polls /api/code
→ Stitchly exchanges code locally and stores tokens locally
```

Set Stitchly/local env values to:

```bash
export TIKTOK_REDIRECT_URI="https://threadback.vercel.app/api/callback"
export TIKTOK_CALLBACK_CODE_URL="https://threadback.vercel.app/api/code"
```

## Testing TikTok API calls

Once the local token file exists, local scripts can read the access token and call TikTok APIs.

For example, your local tests can call:

```text
GET  /v2/user/info/
POST /v2/video/list/
```

TikTok can return an `error` object with `code: "ok"` on successful responses. Do not treat every `error` object as a failure; check the `code` field.

Keep API testing scripts local or commit only generic reusable versions that do not include secrets or tokens.

## Git safety checks

Before committing, check that local secret/token files are ignored:

```bash
git check-ignore .env.tiktok .tiktok_tokens.json .env.local
```

They should be ignored.

Recommended commit:

```bash
git add README.md package.json vercel.json api/ public/ index.html privacy.html terms.html scripts/ .gitignore .env.example
git commit -m "Set up threadback OAuth callback utility"
```

## Manual redeploy

After changing pages or callback code:

```bash
vercel --prod
```

## Notes

* Threadback is designed for sandbox/dev OAuth testing.
* The callback endpoint stores returned OAuth codes temporarily by `state`.
* `/api/code` returns and optionally consumes the short-lived code for local scripts.
* Token exchange is done locally by `scripts/tiktok_exchange_code.py` or by a local Stitchly pipeline.
* TikTok client secrets should stay in local env files or local pipeline secret storage.
* Access and refresh tokens should stay in local ignored files.
* Replace placeholder privacy and terms pages before any production usage.
