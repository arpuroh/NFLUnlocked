// Kicks off the one-time Yahoo OAuth flow. Visit /api/auth-start in a browser.
module.exports = (req, res) => {
  const clientId = process.env.YAHOO_CLIENT_ID;
  if (!clientId) {
    res.status(500).send(
      "YAHOO_CLIENT_ID is not set. Add it in Vercel → Project → Settings → Environment Variables, then redeploy."
    );
    return;
  }
  const redirectUri = `https://${req.headers.host}/api/auth-callback`;
  const url =
    "https://api.login.yahoo.com/oauth2/request_auth" +
    `?client_id=${encodeURIComponent(clientId)}` +
    `&redirect_uri=${encodeURIComponent(redirectUri)}` +
    "&response_type=code&language=en-us";
  res.writeHead(302, { Location: url });
  res.end();
};
