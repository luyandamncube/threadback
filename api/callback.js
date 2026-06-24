export default function handler(req, res) {
  const { code, state, scopes, scope, error, error_description } = req.query;

  res.setHeader("Content-Type", "text/html; charset=utf-8");
  res.setHeader("Cache-Control", "no-store");

  if (error) {
    return res.status(400).send(renderPage({
      title: "TikTok auth error",
      sections: [
        ["error", error],
        ["description", error_description || ""],
      ],
      footer: "Return to your terminal/app and try the auth flow again."
    }));
  }

  return res.status(200).send(renderPage({
    title: "TikTok auth callback received",
    intro: "Copy this code back into your local token exchange script.",
    sections: [
      ["code", code || ""],
      ["state", state || ""],
      ["scopes", scopes || scope || ""],
    ],
    footer: "You can close this tab after copying the code."
  }));
}

function renderPage({ title, intro = "", sections = [], footer = "" }) {
  const blocks = sections.map(([label, value]) => `
    <h3>${escapeHtml(label)}</h3>
    <pre style="white-space: pre-wrap; word-break: break-word; padding: 12px; background: #f4f4f4; border-radius: 8px;">${escapeHtml(value)}</pre>
  `).join("\n");

  return `
    <html>
      <head>
        <title>${escapeHtml(title)}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body style="font-family: system-ui, sans-serif; line-height: 1.5; max-width: 760px; margin: 40px auto; padding: 0 16px;">
        <h1>${escapeHtml(title)}</h1>
        ${intro ? `<p>${escapeHtml(intro)}</p>` : ""}
        ${blocks}
        ${footer ? `<p>${escapeHtml(footer)}</p>` : ""}
      </body>
    </html>
  `;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}
