export default function handler(req, res) {
  res.setHeader("Content-Type", "text/html; charset=utf-8");
  res.setHeader("Cache-Control", "no-store");

  return res.status(200).send(`
    <html>
      <head>
        <title>Threadback OAuth Callback</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body style="font-family: system-ui, sans-serif; line-height: 1.5; max-width: 760px; margin: 40px auto; padding: 0 16px;">
        <h1>Threadback OAuth Callback</h1>
        <p>Use <code>/api/callback</code> as the OAuth redirect URI.</p>
        <p>Local scripts can poll <code>/api/code?state=...</code> to fetch the short-lived code.</p>
      </body>
    </html>
  `);
}
