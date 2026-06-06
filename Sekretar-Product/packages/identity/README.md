# Identity Package

Production-oriented Python foundation for the SekretaR Identity block.

This package intentionally contains no FastAPI endpoints, ORM models, database migrations, JWT/OAuth implementation, or product block integration.

Phase 1 covers:

- Account;
- User;
- UserProfile;
- AccountMembership;
- Device;
- DeviceGrant;
- Session;
- BetaAccess;
- IdentityEvent;
- repository interfaces;
- policies;
- service layer;
- test-only in-memory repositories.

The business logic is designed to receive a PostgreSQL/ORM persistence implementation later without rewriting Identity rules.
