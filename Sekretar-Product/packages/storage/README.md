# Storage Package

Storage abstraction lives here.

Runtime storage must not be part of application code.

Storage categories:

- raw audio;
- upload chunks;
- transcripts;
- summaries;
- model artifacts;
- exports;
- research artifacts;
- temporary files.

Database records should store storage keys, metadata, checksums, ownership, and retention policy rather than embedding files directly.
