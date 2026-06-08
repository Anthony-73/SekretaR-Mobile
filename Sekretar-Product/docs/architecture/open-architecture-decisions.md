# Open Architecture Decisions

## Purpose

Этот документ хранит архитектурные хвосты, которые нельзя потерять, но которые не должны блокировать текущий этап реализации.

Здесь фиксируются:

- открытые архитектурные решения;
- отложенные вопросы;
- future capabilities;
- решения, которые нужно пересмотреть перед соответствующим блоком.

## Rules

1. Мелкие доменные инварианты исправляются сразу, если это дешево и влияет на текущую модель.
2. Крупные будущие возможности фиксируются здесь, а не держатся в чате.
3. Каждый пункт должен иметь:
   - ID;
   - статус;
   - область;
   - краткое описание;
   - почему отложено;
   - когда вернуться.
4. После реализации пункт закрывается или переносится в соответствующий архитектурный документ.

## Statuses

- `OPEN` — вопрос открыт, решение не принято.
- `DEFERRED` — направление понятно, реализация отложена до соответствующего блока.
- `RESOLVED` — решение принято и реализовано.
- `SUPERSEDED` — решение заменено более новым документом или архитектурой.

## Initial Items

### OAD-001 — CandidateKnowledge merge trace

**Status:** RESOLVED

**Area:** Memory / CandidateKnowledge

**Decision:**
CandidateKnowledge with `MERGED` status must always have `merged_into_knowledge_id`.

**Reason:**
A merged candidate must not lose traceability to the KnowledgeItem it was merged into.

**Resolution:**
Implemented in commit `a0f8ea25d16a083ac5bff5f8c7d964a73083a4dd`.

## Future Items

### OAD-002 — Nafanya Memory Adaptation

**Status:** DEFERRED

**Area:** Cross-Project Architecture

**Description:**
После завершения Memory Foundation исследовать перенос архитектурных принципов Memory в проект Nafanya.

**Transfer:**
- Source
- Candidate
- Provenance
- Confidence
- Lifecycle
- Context

**Do Not Transfer:**
- код Sekretar-Product `packages/memory` напрямую;
- корпоративную Account-модель Sekretar.

**Why Deferred:**
Nafanya требует отдельного проектирования долговременной памяти с собственной доменной моделью. Перенос возможен только после завершения Memory Foundation в Sekretar.

**Return When:**
Перед началом проектирования долговременной памяти Nafanya.

### OAD-003 — Trust Calibration

**Status:** DEFERRED

**Area:** Cross-cutting Architecture / Memory / Assistant / Research

**Decision:**
Trust Calibration is a separate architectural axis from per-knowledge
Confidence and from Provenance.

It describes the maturity of the evidence environment for an Account and
working context, not the trustworthiness of a single knowledge claim.

**Principles:**
- does not replace Confidence;
- is not part of Provenance;
- applies to Account and context maturity (Speaker Intelligence, User Context,
  Meetings quality, cross-source reinforcement);
- will be consumed by future MemoryContext, Assistant, and Research;
- in cold-start conditions the product must not behave as if Memory is already
  mature.

**Why Deferred:**
Trust Calibration requires signals from blocks that are not yet implemented
(Meetings quality, Speaker Intelligence maturity, User Context). Memory
Foundation can proceed with claim-level Confidence and Provenance first.

**Return When:**
Before designing MemoryContext policy, Assistant context orchestration, and
Research internal-context weighting.

### OAD-004 — Clarification Flow

**Status:** DEFERRED

**Area:** Cross-cutting Architecture / Product Orchestration

**Decision:**
Clarification Flow is an orchestration layer for resolving high-value
uncertainty with the user. It is not a Memory domain entity.

**Principles:**
- lives between Memory, Meetings, Tasks, Assistant, and UI;
- does not show all system doubts;
- uses a limited clarification budget;
- default maximum of 3 clarifications per session;
- selects candidates by expected clarification value, not by lowest confidence
  alone;
- accelerates Memory maturation without model retraining;
- user answers produce Memory outcomes (accept, reject, correct, defer) and
  provenance events.

**Why Deferred:**
Clarification orchestration depends on post-meeting ingestion flows, UI
session design, and ranking policy. Memory Foundation should first complete
CandidateKnowledge, Provenance, and provenance history.

**Return When:**
Before post-meeting clarification UX and Product API orchestration for
candidate review.
