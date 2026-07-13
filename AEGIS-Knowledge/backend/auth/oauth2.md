# OAuth2

- Authorization Code + PKCE for browser and mobile clients (never Implicit flow — it's deprecated for good reason).
- Client Credentials flow for machine-to-machine calls with no user in the loop.
- Validate the `scope` claim on every resource access, not just at token issuance — scope can be narrower than the full grant.
- Store refresh tokens securely (httpOnly cookie or secure storage), never in `localStorage` for browser clients.
