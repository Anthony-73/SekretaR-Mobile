# Backups

Backup and restore planning lives here.

Required backup targets:

- PostgreSQL;
- object or filesystem storage;
- queue state when needed;
- configuration outside git;
- integration credentials outside git.

Backups must support migration from laptop development to a physical 24/7 server.
