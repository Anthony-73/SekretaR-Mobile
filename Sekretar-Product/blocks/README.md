# Blocks

Blocks describe architectural areas of responsibility.

They may initially live in one repository, one database, and one server, but they should remain conceptually separate. This prevents Product API from becoming the central monolith.

The word "block" is used intentionally for responsibility areas.

Foundation 0.3 required blocks:

- Identity;
- Security;
- Security Intelligence;
- Billing;
- Capability Service;
- Meetings;
- Tasks;
- Jobs;
- Memory;
- Projects;
- Goals;
- User Context;
- Research Intelligence;
- Assistant;
- Voice;
- Speaker Intelligence;
- External LLM Gateway;
- Integrations.
