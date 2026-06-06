# Architecture Decisions

Architecture Foundation: 0.3

This document records initial architecture decisions for the new SekretaR Product skeleton.

## Decision 1: Product API Is Not The Central Brain

Product API is the public entry point and lifecycle coordinator.

Heavy processing, memory consolidation, research, integrations, and long-running work must run through Worker or dedicated blocks.

## Decision 2: Meeting Is Not The Product Center

Meeting is an important source and event, but SekretaR is designed as a personal knowledge and action system.

Memory, tasks, projects, goals, research, and assistant capabilities must not be hidden inside the Meetings block.

## Decision 3: Worker And Queue Are Mandatory

Long-running work must be represented as jobs.

This includes meeting processing, STT, diarization, speaker matching, Local LLM processing, memory extraction, research jobs, External LLM calls, exports, integrations, and retries.

## Decision 4: Memory Is Independent

Memory has its own model, lifecycle, provenance, confidence, correction, deletion, and consolidation rules.

Meeting can be a source of Memory, but does not own Memory.

Speaker Intelligence can provide processed participant information to Memory, but Memory does not own diarization or voice matching.

## Decision 5: Local LLM And External LLM Are Separate

Local LLM works near Whisper and supports meeting processing.

External LLM is accessed through External LLM Gateway and is used for Research Intelligence, complex reasoning, and future assistant capabilities.

## Decision 6: Speaker Intelligence Is Independent

Speaker Intelligence is a separate block for diarization, anonymous speaker labels, voice fingerprints, cross-meeting speaker matching, and gradual participant identification.

The first stage should not assume known participant names. It should create anonymous speakers such as `Speaker_1`, `Speaker_2`, and `Speaker_3`, then improve identity links over time.

The target flow is:

Recording -> STT -> Speaker Intelligence -> Structured Transcript -> Summary -> Tasks -> Memory

## Decision 7: Configuration Uses Environment Variables

Configuration must come from environment variables.

No IP addresses, tokens, credentials, or secrets should be hardcoded.

## Decision 8: Runtime Storage Is Outside Code

Audio, chunks, transcripts, summaries, exports, temporary files, and research artifacts must live in runtime storage, not in application source directories.

## Decision 9: Virtual Environments Are Outside Repository

Virtual environments and dependency caches must not be committed.

## Decision 10: Initial Database Split Is Logical

The preferred first step is one PostgreSQL database with separate schemas for responsibility blocks.

Suggested schemas:

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

Physical separation can be considered later if Memory or search workload requires it.

## Decision 11: Capability Service Is Required

SekretaR will have multiple clients over time.

Capability Service must manage compatibility for Web App, Android Recorder, future iOS Recorder, Browser Recorder, Desktop Recorder, API contracts, and feature flags.

Capability Service also uses Identity and Billing data to determine available functions, limits, and required updates.

## Decision 12: Identity Is The Root User Block

Identity owns registration, login, accounts, users, devices, sessions, recovery, and account deletion.

Beta 1 uses access codes and `device_id`.

Beta 2 moves to full accounts, managed devices, and account-owned data.

All product data belongs to User Account, not to a device.

## Decision 13: Security Is Separate From Identity

Identity identifies users and devices.

Security protects APIs, Recorder, Upload, Memory, integrations, and runtime access.

Security owns access control, Trust Score usage, rate limits, bans, Deception Corridor, canary assets, and incident response.

## Decision 14: Security Intelligence Is Separate From Security

Security enforces protection.

Security Intelligence analyzes internal SekretaR security events, API abuse, upload abuse, suspicious user and device patterns, and recommends threat model updates.

Security Intelligence does not attack external systems and does not scan external resources.

## Decision 15: Trust Score Is A Core Security Concept

Each user, device, and session may have a Trust Score.

Security uses Trust Score to make decisions about access, rate limits, upload limits, feature restrictions, and bans.

## Decision 16: Deception Corridor Is Controlled And Data-Safe

Deception Corridor is a controlled false-interest path for hostile behavior.

The sequence is:

1. real protection barrier;
2. controlled false points of interest;
3. Security Events;
4. Security Intelligence;
5. Trust Score;
6. access restriction;
7. ban.

No real user data may be used inside Deception Corridor.

## Decision 17: Billing Is Separate From Authorization And Security

Billing owns virtual credits, real credits, tariffs, packages, trials, limits, accrual history, spending history, and future payment systems.

Billing does not authorize users and does not enforce security.

Billing informs Capability Service about available user features and limits.

## Decision 18: Beta Billing Uses Virtual Credits

Beta 2 should provide users with a starting test balance.

Virtual credits model future product economics before real payments are connected.

The goal is to measure consumption, scenario cost, perceived value, and Billing behavior.

## Decision 19: Free Mode And Credit Mode Coexist

New users receive an introductory period with full access.

After the introductory period, users may stay on a free tier or use credits.

Free mode may include Recorder, file upload, transcription, history, and calendar.

Memory, Research Intelligence, Assistant, and Voice Assistant may use credits.
