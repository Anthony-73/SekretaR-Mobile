# Architecture Blocks

Architecture Foundation: 0.3

This document lists the main SekretaR blocks.

The word "block" means an area of responsibility. Blocks may live in one repository and on one physical server at first, but they should keep separate responsibilities and contracts.

The center of the system is:

User -> Memory -> Research -> Assistant -> Actions

## Identity

Root user block.

Owns registration, login, accounts, `user_id`, devices, `device_id`, device management, sessions, access recovery, and account deletion.

Beta 1 uses access code and `device_id`.

Beta 2 introduces full accounts, users, managed devices, session lifecycle, access recovery, and account deletion.

All data belongs to User Account, not to a device.

Identity is not Security.

## Security

Protection block.

Owns access control, API protection, Recorder protection, Upload protection, Memory protection, integration protection, Trust Score usage, rate limits, ban management, Deception Corridor, canary assets, and incident response.

Security is not Identity.

## Security Intelligence

Internal security analysis block.

Analyzes intrusion attempts, security events, API abuse, upload abuse, suspicious user/device/session patterns, threat model updates, and protection recommendations.

Security Intelligence works only from internal SekretaR events. It does not attack or scan external systems.

## Billing

Product economy block.

Owns virtual credits, real credits, tariffs, packages, trial periods, limits, accrual history, spending history, and future payment systems.

Billing does not authorize users and does not enforce security.

Billing provides Capability Service with available feature and limit information.

## Product API

Entry point for product clients.

Owns:

- public API contracts;
- user and device access;
- meeting lifecycle orchestration;
- upload session creation;
- task confirmation;
- status reads;
- job creation.

Does not own:

- STT;
- diarization;
- voice fingerprinting;
- Local LLM execution;
- External LLM research;
- long-term memory consolidation;
- runtime file storage.

Product API is an entry door and orchestration layer. It must not become the central brain or hidden monolith.

## Web App

Browser interface for meetings, tasks, memory, research, and future assistant features.

It should call Product API only.

## Recorder Android

Recorder V2 is a product app and the beginning of the meeting lifecycle.

It is responsible for recording, local upload state, chunk upload, retry, resume, device identity, and capability metadata.

## AI Processing

Local AI computation block.

Uses Whisper and Local LLM for:

- transcription;
- structured transcript preparation;
- summary;
- task extraction;
- meeting structuring;
- memory candidate extraction.

The target meeting processing flow is:

Recording -> STT -> Speaker Intelligence -> Structured Transcript -> Summary -> Tasks -> Memory

## Speaker Intelligence

Speaker Intelligence is responsible for diarization and participant intelligence.

At the first stage, participant names are unknown. The system creates anonymous labels such as `Speaker_1`, `Speaker_2`, and `Speaker_3`.

Responsibilities:

- diarization;
- separating participants by voice;
- voice fingerprints;
- matching voices across meetings;
- gradual participant identification;
- linking repeated participants between meetings;
- passing processed participant information to Memory;
- helping identify authors of decisions and tasks.

Speaker Intelligence is not part of Memory. Memory receives its processed output and uses it as one source of knowledge.

## Worker

Executes queued work.

Required job categories:

- meeting processing;
- STT;
- summary;
- task extraction;
- memory extraction;
- memory consolidation;
- research jobs;
- External LLM calls;
- exports;
- calendar integrations;
- retries.

## Memory

Independent user memory block.

Memory stores:

- user facts;
- project knowledge;
- decision history;
- knowledge about people and contacts;
- links between entries;
- source provenance;
- change history;
- confidence;
- deletion and correction state.

Meeting is only one source of memory.

Memory may receive participant signals from Speaker Intelligence, but it does not perform diarization or voice matching itself.

Memory owns facts, decisions, project context, participant knowledge, object links, interaction history, and memory search.

Memory does not own STT, Recorder, Speaker Intelligence, or external LLM access.

Memory must be designed so it can later move to separate storage or a separate database without changing the rest of the architecture.

## Projects

Project knowledge block.

Connects tasks, meetings, memory entries, participants, research briefings, decisions, and goals.

## Goals

Long-term intention block.

Goals are not tasks. Goals describe intended outcomes and can connect to projects, tasks, Memory, Assistant, and Research.

## User Context

Current context block.

Represents active focus, recent activity, relevant memory, active projects, active tasks, and assistant context windows.

## Research Intelligence

External research block for confirmed tasks.

It prepares short research briefings from external sources and asks the user before deeper research.

It is not ordinary chat and not primarily a search system for past meetings.

It does not perform actions on behalf of the user automatically.

## External LLM Gateway

Gateway for external API models.

It provides model/provider abstraction, cost controls, privacy filtering, retries, and model run logs.

External LLM should be independently replaceable from Local LLM.

External LLM Gateway is used by Research Intelligence, Assistant, and future advanced reasoning. It should not replace Local LLM for ordinary meeting processing.

## Capability Service

Compatibility and version block.

Manages:

- Web App versions;
- Android Recorder versions;
- future iOS, Desktop, and Browser Recorder versions;
- API contract versions;
- feature flags;
- upload protocol capabilities.

Capability Service also uses Identity and Billing information to determine available user features, limits, feature flags, and required client updates.

## Integrations

External product connections such as calendar, exports, documents, email, CRM, and future data providers.

## Assistant

Future text and voice assistant block.

Uses Memory, User Context, Research Intelligence, and External LLM Gateway.

Assistant does not own Memory.

## Voice

Future voice interface block.

Uses Assistant, Memory, Research Intelligence, User Context, and speech interfaces.

## Future Blocks

Assistant, Voice, User Context, Projects, and Goals are reserved as separate blocks.

They should not be implemented inside Meetings or Product API as hidden subfeatures.
