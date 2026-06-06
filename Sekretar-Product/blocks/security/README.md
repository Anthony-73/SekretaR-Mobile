# Security Block

Security protects SekretaR APIs, clients, uploads, Memory, integrations, and runtime access.

Security is separate from Identity. Identity knows who the user and device are. Security decides whether a request, session, user, or device should be trusted.

## Responsibilities

- access control;
- Product API protection;
- Recorder protection;
- Upload protection;
- Memory protection;
- integration protection;
- Trust Score usage;
- rate limits;
- ban management;
- deception corridor;
- canary assets;
- incident response.

## Trust Score

Each user, device, and session can have a Trust Score.

Security uses Trust Score to decide:

- allowed operations;
- rate limits;
- upload limits;
- challenge requirements;
- feature availability restrictions;
- temporary or permanent bans.

## Deception Corridor

Deception Corridor is a controlled false-interest path for hostile behavior.

The logic is:

1. real protection barrier;
2. controlled false points of interest;
3. Security Events;
4. Security Intelligence;
5. Trust Score update;
6. access restriction;
7. ban.

No real user data may be used inside Deception Corridor.

## Non-Responsibilities

- account registration;
- password or session ownership;
- billing credits;
- external system attacks or scans;
- external threat hunting outside SekretaR.
