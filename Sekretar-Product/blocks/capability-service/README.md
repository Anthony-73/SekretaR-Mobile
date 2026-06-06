# Capability Service Block

Capability Service manages compatibility across SekretaR clients and API contracts.

Recorder is one client inside the product ecosystem, not a separate product.

Responsibilities:

- Web App version compatibility;
- Android Recorder compatibility;
- future iOS, Desktop, and Browser Recorder compatibility;
- API contract versions;
- feature flags;
- upload protocol selection;
- audio format and chunk size limits;
- forced update decisions.
- available user functions;
- Billing-aware limits;
- Identity-aware account and device state.

Clients should check capabilities before using product workflows.

Capability Service receives signals from Identity and Billing, but it does not own accounts or credits.
