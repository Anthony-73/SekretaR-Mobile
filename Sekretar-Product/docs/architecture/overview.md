# SekretaR Architecture Overview

Architecture Foundation: 0.3

SekretaR is a platform for personal memory, knowledge, research, and actions.

The product is not centered on meetings. A meeting is an important event and source of knowledge, but it is only one source among recordings, dialogs, documents, tasks, calendar events, and future integrations.

The center of the system is:

User -> Memory -> Research -> Assistant -> Actions

## Product Direction

The planned development sequence is:

1. new architecture skeleton;
2. Worker and Queue;
3. User Memory;
4. Research Intelligence;
5. Voice Assistant.

## Main Flow

Recorder Android starts the meeting lifecycle.

The expected lifecycle is:

1. Recorder creates or receives meeting identity.
2. Recorder records audio and uploads it through Product API.
3. Product API creates upload and processing jobs.
4. Worker executes long-running work.
5. AI Processing performs STT.
6. Speaker Intelligence performs diarization, speaker separation, and voice fingerprinting.
7. AI Processing produces a structured transcript, summary, tasks, and meeting structure.
8. Meeting artifacts are stored in Storage and referenced in PostgreSQL.
9. Memory jobs receive processed participant information and consolidate long-term user knowledge.
10. Confirmed tasks may trigger Research Intelligence.
11. Web App, future Assistant, and future Voice use Product API and block contracts.

The target meeting intelligence flow is:

Recording -> STT -> Speaker Intelligence -> Structured Transcript -> Summary -> Tasks -> Memory

## Identity Direction

Identity is the root user block.

Beta 1 uses access codes and `device_id`.

Beta 2 introduces full user accounts, account-owned data, managed devices, sessions, access recovery, and account deletion.

All product data belongs to the User Account, not to an individual device.

## Security Direction

Security is separate from Identity.

Security protects APIs, Recorder, Upload, Memory, integrations, and runtime access. It owns access control, Trust Score usage, rate limits, ban management, Deception Corridor, canary assets, and incident response.

Security Intelligence is separate from Security. It analyzes internal SekretaR security events, abuse patterns, suspicious user and device behavior, and weekly security review data. It does not attack or scan external systems.

## Billing Direction

Billing is separate from Identity and Security.

Beta 2 should use virtual credits to model product economics before real payments. Production may keep the credit model with packages such as 20, 40, and 100 credits.

New users should have an introductory period with full access. After that, free mode may keep Recorder, file upload, transcription, history, and calendar, while Memory, Research Intelligence, Assistant, and Voice Assistant may use credits.

Billing provides Capability Service with information about available user features and limits.

## Product API Role

Product API is the public entry point. It is not the central brain.

It should coordinate product lifecycle, access control, validation, and public contracts. It should delegate heavy processing, memory consolidation, research work, exports, and integrations to Worker and dedicated blocks.

Product API must not become a hidden monolith for Memory, Research, Assistant, Security Intelligence, Billing, or Speaker Intelligence.

## Runtime Target

The project must support:

- local development on a laptop;
- migration to a physical server;
- 24/7 operation;
- remote administration;
- future scale-out;
- no permanent dependence on a temporary VPS.

## Configuration

All configuration must come from environment variables. IP addresses, tokens, secrets, and credentials must not be hardcoded.

Runtime storage and virtual environments must not be committed to the repository.
