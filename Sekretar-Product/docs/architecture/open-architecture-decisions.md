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
