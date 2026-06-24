#!/usr/bin/env python3

from pathlib import Path
from datetime import date
import shutil

PROJECT_NAME = "Threadback"
TAGLINE = "A tiny OAuth callback postbox for dev flows."
TODAY = date.today().isoformat()

ROOT = Path.cwd()
PUBLIC = ROOT / "public"

PAGES = {
    "index.html": {
        "title": "Threadback",
        "heading": "Threadback",
        "body": f"""
          <p class="lede">{TAGLINE}</p>

          <p>
            Threadback is a small developer utility used to receive OAuth callback redirects
            during local and sandbox API testing.
          </p>

          <p>
            It is intended for development workflows where an OAuth provider needs a public
            HTTPS redirect URL, but the token exchange and API testing are handled locally.
          </p>

          <div class="card">
            <h2>Useful links</h2>
            <ul>
              <li><a href="/api/callback">OAuth callback endpoint</a></li>
              <li><a href="/privacy.html">Privacy Policy</a></li>
              <li><a href="/terms.html">Terms of Use</a></li>
            </ul>
          </div>

          <p class="muted">
            This is a placeholder landing page for developer testing.
          </p>
        """,
    },
    "privacy.html": {
        "title": "Privacy Policy | Threadback",
        "heading": "Privacy Policy",
        "body": f"""
          <p class="muted">Last updated: {TODAY}</p>

          <p>
            Threadback is a developer testing utility for receiving OAuth callback redirects.
            This placeholder policy describes the intended test usage of this project.
          </p>

          <h2>Information received</h2>
          <p>
            When an OAuth provider redirects to Threadback, the callback URL may include
            temporary query parameters such as an authorization code, state value, scope,
            or error details.
          </p>

          <h2>How information is used</h2>
          <p>
            The callback page displays the received OAuth parameters in the browser so the
            developer can copy them into a local test script. Threadback does not intentionally
            store, sell, or share this information.
          </p>

          <h2>Developer responsibility</h2>
          <p>
            OAuth authorization codes and tokens can be sensitive. Developers using this
            project should avoid sharing callback URLs, logs, screenshots, or copied codes
            publicly.
          </p>

          <h2>Contact</h2>
          <p>
            This is a placeholder page for development and sandbox testing. Replace this
            section with your real contact details before using the project in production.
          </p>

          <p class="muted">
            This placeholder is not legal advice. Replace it with a reviewed policy before
            using Threadback with real users.
          </p>
        """,
    },
    "terms.html": {
        "title": "Terms of Use | Threadback",
        "heading": "Terms of Use",
        "body": f"""
          <p class="muted">Last updated: {TODAY}</p>

          <p>
            Threadback is provided as a lightweight developer utility for OAuth callback
            testing and sandbox API experiments.
          </p>

          <h2>Permitted use</h2>
          <p>
            You may use Threadback to test OAuth redirect flows, inspect callback parameters,
            and support local development workflows.
          </p>

          <h2>Not for production use</h2>
          <p>
            This placeholder deployment is not intended for production authentication,
            long-term credential handling, or use with real end users without additional
            security, privacy, and legal review.
          </p>

          <h2>No warranty</h2>
          <p>
            Threadback is provided as-is for development testing. No guarantee is made that
            it is secure, available, or suitable for any specific purpose.
          </p>

          <h2>Third-party services</h2>
          <p>
            OAuth providers and API platforms may have their own terms, policies, and
            developer requirements. You are responsible for complying with those requirements.
          </p>

          <p class="muted">
            This placeholder is not legal advice. Replace it with reviewed terms before
            using Threadback with real users.
          </p>
        """,
    },
}

CSS = """
:root {
  color-scheme: light dark;
  --bg: #f7f4ef;
  --text: #1f2933;
  --muted: #5f6c7b;
  --card: #ffffff;
  --border: #ddd6cc;
  --accent: #6f4bd8;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: #111318;
    --text: #f4f4f5;
    --muted: #a1a1aa;
    --card: #181b22;
    --border: #2b303b;
    --accent: #a78bfa;
  }
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.65;
}

main {
  max-width: 760px;
  margin: 0 auto;
  padding: 56px 20px;
}

nav {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
  margin-bottom: 40px;
  font-size: 0.95rem;
}

a {
  color: var(--accent);
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

h1 {
  font-size: clamp(2.2rem, 6vw, 4rem);
  line-height: 1;
  letter-spacing: -0.05em;
  margin: 0 0 20px;
}

h2 {
  margin-top: 36px;
  letter-spacing: -0.02em;
}

p {
  margin: 16px 0;
}

.lede {
  font-size: 1.25rem;
  color: var(--muted);
}

.muted {
  color: var(--muted);
  font-size: 0.95rem;
}

.card {
  margin: 28px 0;
  padding: 20px;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
}

footer {
  margin-top: 56px;
  padding-top: 24px;
  border-top: 1px solid var(--border);
  color: var(--muted);
  font-size: 0.9rem;
}
"""

def page_template(title: str, heading: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <style>
{CSS}
  </style>
</head>
<body>
  <main>
    <nav>
      <a href="/index.html">Home</a>
      <a href="/api/callback">Callback</a>
      <a href="/privacy.html">Privacy</a>
      <a href="/terms.html">Terms</a>
    </nav>

    <h1>{heading}</h1>

    {body}

    <footer>
      {PROJECT_NAME} — {TAGLINE}
    </footer>
  </main>
</body>
</html>
"""

def write_pages(target_dir: Path) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)

    for filename, page in PAGES.items():
        html = page_template(
            title=page["title"],
            heading=page["heading"],
            body=page["body"],
        )
        path = target_dir / filename
        path.write_text(html, encoding="utf-8")
        print(f"wrote {path}")

def main() -> None:
    write_pages(ROOT)

    # Mirror to public/ for Vercel static hosting.
    write_pages(PUBLIC)

    print()
    print("Done.")
    print("Suggested git commands:")
    print("  git add index.html privacy.html terms.html public/")
    print('  git commit -m "Add placeholder public pages"')

if __name__ == "__main__":
    main()
