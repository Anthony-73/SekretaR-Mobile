# Migration Plan

Architecture Foundation: 0.3

This plan describes the recommended order for moving from the current audited state to the new SekretaR Product skeleton.

No migration is performed by this skeleton.

## Principles

- Do not copy old code blindly.
- Do not keep `main.py` as a long-term architecture center.
- Do not store secrets in code.
- Do not store virtual environments in the repository.
- Do not store runtime files as application code.
- Do not hardcode IP addresses.
- Keep Identity, Security, Security Intelligence, Billing, Product API, AI Processing, Speaker Intelligence, Worker, Memory, and Research as separate blocks.

## Suggested Order

1. Keep this skeleton as the target structure.
2. Define environment variables and deployment conventions.
3. Define API contracts for Identity, Recorder, upload lifecycle, meeting status, jobs, speaker intelligence results, tasks, memory sources, research jobs, billing capabilities, security events, and client capabilities.
4. Create database schemas for `core`, `identity`, `security`, `meetings`, `jobs`, `speakers`, `memory`, `research`, `billing`, `integrations`, and `capabilities`.
5. Build Identity transition path from Beta 1 access code/device model to Beta 2 account/device model.
6. Build Product API as a thin entry point and lifecycle coordinator.
7. Move current AI processing ideas into `apps/ai-processing` as a separate service.
8. Add Worker and Queue before adding new heavy features.
9. Implement upload lifecycle and processing jobs.
10. Integrate Recorder Android through capability-aware contracts.
11. Add Security events, Trust Score, rate limits, and incident records.
12. Add Speaker Intelligence after STT and before summary/task extraction.
13. Add Memory extraction and consolidation using structured transcript and participant signals.
14. Add Billing virtual credits for Beta 2.
15. Add Research Intelligence for confirmed tasks.
16. Add future Assistant and Voice blocks after Memory and Research have stable contracts.

## What To Bring Forward Later

- Whisper and STT pipeline ideas.
- Diarization, anonymous speaker labels, and voice fingerprinting as a new responsibility block.
- Local LLM summary and task extraction ideas.
- Chunk upload protocol ideas.
- Meeting history behavior.
- Beta/device access ideas.
- Google Calendar integration concept.
- Current server frontend direction, after review.
- Recorder V2 product workflow.
- Beta access ideas as an input to the Identity Beta 1 to Beta 2 transition.

## What Not To Bring Forward As-Is

- monolithic `main.py`;
- hardcoded server IPs;
- credentials and tokens;
- virtual environments;
- runtime `data/meetings` as repository content;
- SQLite user service;
- temporary VPS-centered deployment assumptions;
- direct public API calls to heavy AI as the long-term processing model.
- device-owned product data as the long-term identity model.
