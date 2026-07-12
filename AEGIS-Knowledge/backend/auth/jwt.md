# JWT Authentication

- Short-lived access tokens (15 min – 1 hr) plus a longer-lived refresh token — never a single long-lived access token.
- RS256 (asymmetric) when multiple services need to verify tokens independently; HS256 only for a single self-contained service holding the one shared secret.
- Always verify signature, `exp` (expiry), `iss` (issuer), and `aud` (audience) — skipping any of these is a real vulnerability, not a formality.
- Never put sensitive data (passwords, full PII) in the JWT payload — it's base64, not encrypted.
