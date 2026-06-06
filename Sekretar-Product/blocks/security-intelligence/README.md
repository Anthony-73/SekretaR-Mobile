# Security Intelligence Block

Security Intelligence analyzes security events generated inside SekretaR.

It is separate from Security. Security enforces protection. Security Intelligence studies events, patterns, and incidents to improve protection over time.

## Responsibilities

- analyzing intrusion attempts;
- analyzing security events;
- analyzing API abuse;
- analyzing upload abuse;
- analyzing suspicious user, device, and session patterns;
- updating the threat model;
- recommending stronger protections;
- supporting weekly security reviews.

## Boundaries

Security Intelligence works only from internal SekretaR events.

It must not:

- attack external systems;
- scan external resources;
- perform offensive actions;
- use real user data in deception assets.

## Outputs

- threat model updates;
- Trust Score recommendations;
- ban recommendations;
- rate limit recommendations;
- deception corridor findings;
- incident summaries;
- weekly security review inputs.
