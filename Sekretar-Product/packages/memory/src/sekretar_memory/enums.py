"""Memory domain enumerations.

These enums define the architectural surface of the Memory block. They do not
implement storage, retrieval, inference, or lifecycle transition logic.
"""

from enum import Enum


class KnowledgeType(str, Enum):
    """Types of durable knowledge Memory may preserve."""

    FACT = "fact"
    DECISION = "decision"
    PREFERENCE = "preference"
    RESPONSIBILITY = "responsibility"
    PERSON_KNOWLEDGE = "person_knowledge"
    PROJECT_KNOWLEDGE = "project_knowledge"
    COMPANY_KNOWLEDGE = "company_knowledge"
    TEAM_KNOWLEDGE = "team_knowledge"
    CONSTRAINT = "constraint"
    EXPLANATION = "explanation"
    RESEARCH_FINDING = "research_finding"
    CORRECTION = "correction"


class SourceType(str, Enum):
    """Source types that may produce candidate knowledge."""

    MEETING = "meeting"
    DOCUMENT = "document"
    VOICE_NOTE = "voice_note"
    MANUAL_NOTE = "manual_note"
    RESEARCH = "research"
    ASSISTANT_INTERACTION = "assistant_interaction"
    INTEGRATION = "integration"
    CONFIRMED_TASK = "confirmed_task"
    UNKNOWN = "unknown"


class KnowledgeStatus(str, Enum):
    """Conceptual lifecycle states for knowledge.

    CANDIDATE is reserved for CandidateKnowledge and must not be used on
    accepted KnowledgeItem instances.
    """

    CANDIDATE = "candidate"
    ACTIVE = "active"
    CONFIRMED = "confirmed"
    UNCONFIRMED = "unconfirmed"
    OUTDATED = "outdated"
    CONTRADICTED = "contradicted"
    CORRECTED = "corrected"
    ARCHIVED = "archived"
    DELETED = "deleted"
    FORGOTTEN = "forgotten"


class ConfidenceLevel(str, Enum):
    """Product-level confidence labels for knowledge."""

    CONFIRMED = "confirmed"
    STRONGLY_SUPPORTED = "strongly_supported"
    INFERRED = "inferred"
    UNCONFIRMED = "unconfirmed"
    DOUBTFUL = "doubtful"
    CONTRADICTED = "contradicted"


class ProvenanceType(str, Enum):
    """Origin type for knowledge provenance."""

    EXPLICITLY_STATED = "explicitly_stated"
    MODEL_INFERRED = "model_inferred"
    USER_CORRECTED = "user_corrected"
    RESEARCH_DERIVED = "research_derived"
    INTEGRATION_IMPORTED = "integration_imported"


class RelationType(str, Enum):
    """Allowed conceptual relation types between knowledge and references."""

    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    UPDATES = "updates"
    REPLACES = "replaces"
    RELATED_TO = "related_to"
    DERIVED_FROM = "derived_from"
    EXPLAINS = "explains"
    CONCERNS_PERSON = "concerns_person"
    CONCERNS_PROJECT = "concerns_project"
    CONCERNS_TASK = "concerns_task"
    CONCERNS_MEETING = "concerns_meeting"


class CandidateKnowledgeStatus(str, Enum):
    """Lifecycle states for candidate knowledge before acceptance."""

    DETECTED = "detected"
    EVALUATED = "evaluated"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    DEFERRED = "deferred"
    MERGED = "merged"
    CONTRADICTION = "contradiction"


class CandidateRejectionReason(str, Enum):
    """Reasons why candidate knowledge was rejected."""

    LOW_VALUE = "low_value"
    DUPLICATE = "duplicate"
    NOISE = "noise"
    RAW_SOURCE_DUMP = "raw_source_dump"
    USER_REJECTED = "user_rejected"
    CONTRADICTION_UNRESOLVED = "contradiction_unresolved"
    INSUFFICIENT_PROVENANCE = "insufficient_provenance"
    POLICY_BLOCKED = "policy_blocked"


class MemoryEventType(str, Enum):
    """Domain events emitted by the Memory block."""

    CANDIDATE_KNOWLEDGE_DETECTED = "candidate_knowledge_detected"
    KNOWLEDGE_ACCEPTED = "knowledge_accepted"
    KNOWLEDGE_REJECTED = "knowledge_rejected"
    KNOWLEDGE_DEFERRED = "knowledge_deferred"
    KNOWLEDGE_MERGED = "knowledge_merged"
    KNOWLEDGE_CONFIRMED = "knowledge_confirmed"
    KNOWLEDGE_CORRECTED = "knowledge_corrected"
    KNOWLEDGE_CONTRADICTION_DETECTED = "knowledge_contradiction_detected"
    KNOWLEDGE_MARKED_OUTDATED = "knowledge_marked_outdated"
    KNOWLEDGE_ARCHIVED = "knowledge_archived"
    KNOWLEDGE_DELETED = "knowledge_deleted"
    KNOWLEDGE_FORGOTTEN = "knowledge_forgotten"
    KNOWLEDGE_RELATION_CREATED = "knowledge_relation_created"
    MEMORY_CONTEXT_PREPARED = "memory_context_prepared"
    MEMORY_SOURCE_LINKED = "memory_source_linked"
