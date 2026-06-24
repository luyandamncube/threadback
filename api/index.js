export default function handler(req, res) {
  res.setHeader("Content-Type", "text/html; charset=utf-8");

  return res.status(200).send(`
    <html>
      <head>
        <title>Vercel OAuth Callback</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body style="font-family: system-ui, sans-serif; line-height: 1.5; max-width: 760px; margin: 40px auto; padding: 0 16px;">
        <h1>Vercel OAuth Callback</h1>
        <p>This project is a small OAuth callback receiver for local API testing.</p>
        <p>Use the callback endpoint:</p>
        <pre style="white-space: pre-wrap; padding: 12px; background: #f4f4f4; border-radius: 8px;">/api/callback</pre>
      </body>
    </html>
  `);
}
