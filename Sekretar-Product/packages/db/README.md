# Database Package

Database conventions and migration ownership live here.

Initial recommendation:

- one PostgreSQL database;
- separate schemas for responsibility blocks;
- clear ownership of tables;
- migration history;
- no secrets in code.

Likely schemas:

- `core`;
- `identity`;
- `security`;
- `meetings`;
- `jobs`;
- `speakers`;
- `memory`;
- `research`;
- `billing`;
- `integrations`;
- `capabilities`.

Memory must be designed so it can later move to a separate database or specialized storage without changing the rest of the architecture.

Security, Identity, and Billing are separate ownership areas even if they start in the same PostgreSQL database.
