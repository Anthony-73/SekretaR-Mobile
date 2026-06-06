# Config

Configuration conventions live here.

Rules:

- all runtime configuration comes from environment variables;
- `.env.example` documents required variables;
- real `.env` files are not committed;
- IP addresses, tokens, credentials, and secrets are not hardcoded;
- local and server configuration must use the same variable names.
