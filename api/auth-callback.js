// Yahoo redirects here after the commissioner authorizes the app.
// Exchanges the code for tokens and displays the refresh token to copy
// into the GitHub repo secret YAHOO_REFRESH_TOKEN. Nothing is stored.
module.exports = async (req, res) => {
  const { code, error } = req.query || {};
  if (error) {
    res.status(400).send(`Yahoo returned an error: ${error}`);
    return;
  }
  if (!code) {
    res.status(400).send("Missing ?code= from Yahoo. Start again at /api/auth-start.");
    return;
  }
  const clientId = process.env.YAHOO_CLIENT_ID;
  const clientSecret = process.env.YAHOO_CLIENT_SECRET;
  if (!clientId || !clientSecret) {
    res.status(500).send("YAHOO_CLIENT_ID / YAHOO_CLIENT_SECRET env vars are not set in Vercel.");
    return;
  }

  const redirectUri = `https://${req.headers.host}/api/auth-callback`;
  const body = new URLSearchParams({
    client_id: clientId,
    client_secret: clientSecret,
    redirect_uri: redirectUri,
    code,
    grant_type: "authorization_code",
  });

  const resp = await fetch("https://api.login.yahoo.com/oauth2/get_token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: body.toString(),
  });
  const tokens = await resp.json();

  if (!tokens.refresh_token) {
    res
      .status(500)
      .send(`Token exchange failed: ${JSON.stringify(tokens)}. Check the client id/secret and try again.`);
    return;
  }

  res.setHeader("Content-Type", "text/html; charset=utf-8");
  res.send(`<!doctype html>
<html><head><meta charset="utf-8"><title>Yahoo connected — NFL Unlocked</title>
<style>
  body{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;background:#201E1D;color:#F3F2F2;
       display:grid;place-items:center;min-height:100vh;margin:0;padding:24px}
  .card{background:#2A2726;border:1px solid #45413F;padding:32px;max-width:640px}
  h1{margin:0 0 8px;font-size:24px;text-transform:uppercase;letter-spacing:-.01em}
  p{color:#BAB6B6;line-height:1.5}
  code{display:block;background:#151312;border:1px solid #45413F;
       padding:14px;word-break:break-all;margin:16px 0;font-size:13px;color:#FF563C}
  button{background:#EC3013;color:#fff;border:0;padding:10px 18px;
         font-size:15px;font-weight:700;cursor:pointer}
  ol{color:#BAB6B6;line-height:1.7}
</style></head><body><div class="card">
<h1>🏈 Yahoo is connected.</h1>
<p>This is your <strong>refresh token</strong> — the automation uses it to pull league data forever.
It is shown once and stored nowhere. Copy it now:</p>
<code id="tok">${tokens.refresh_token}</code>
<button onclick="navigator.clipboard.writeText(document.getElementById('tok').textContent).then(()=>this.textContent='Copied ✓')">Copy token</button>
<p>Then finish the wiring:</p>
<ol>
<li>Go to your GitHub repo → <strong>Settings → Secrets and variables → Actions</strong></li>
<li>Add/update the secret <strong>YAHOO_REFRESH_TOKEN</strong> with this value</li>
<li>Go to the repo's <strong>Actions</strong> tab → “Update league data” → <strong>Run workflow</strong></li>
<li>In ~1 minute the site shows your real league. You never touch this again.</li>
</ol>
</div></body></html>`);
};
