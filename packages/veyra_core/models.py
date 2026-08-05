from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class EvidenceRole(str, Enum):
    FOR = "for_proceeding"
    AGAINST = "against_proceeding"
    MISSING = "missing"
    CONTEXT = "context"
    UNKNOWN = "unknown"


class ReadinessStatus(str, Enum):
    READY = "ready"
    READY_FOR_LIMITED_TEST = "ready_for_limited_test"
    NOT_READY = "not_ready"
    NEEDS_REVIEW = "needs_review"


class Confidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass(frozen=True)
class SourceRef:
    system: str
    record_id: str
    ingested_at: datetime | None = None


@dataclass(frozen=True)
class AssetRef:
    asset_id: str
    asset_type: str = "unknown"
    subsystem: str | None = None


@dataclass(frozen=True)
class CanonicalEvent:
    event_id: str
    source: SourceRef
    event_type: str
    occurred_at: datetime
    asset: AssetRef
    summary: str
    anchors: dict[str, str] = field(default_factory=dict)
    severity: str = "info"
    evidence_role: EvidenceRole = EvidenceRole.UNKNOWN
    measurements: dict[str, Any] = field(default_factory=dict)
    raw_ref: str | None = None

    @property
    def sortable_key(self) -> tuple[datetime, str]:
        return (self.occurred_at, self.event_id)


@dataclass(frozen=True)
class Relationship:
    from_event_id: str
    to_event_id: str
    relation_type: str
    reason: str
    confidence: Confidence = Confidence.HIGH


@dataclass(frozen=True)
class ReviewRequest:
    review_id: str
    question: str
    asset_id: str
    requested_at: datetime
    window_start: datetime
    window_end: datetime
    required_evidence: list[str] = field(default_factory=list)
    anchors: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class EvidenceItem:
    event_id: str
    label: str
    role: EvidenceRole
    occurred_at: datetime | None
    source_system: str
    summary: str
    reason: str


@dataclass(frozen=True)
class SimilarCase:
    event_id: str
    occurred_at: datetime
    summary: str
    outcome: str | None
    reason: str


@dataclass(frozen=True)
class AISummary:
    answer: str
    cited_event_ids: list[str]
    uncertainty: list[str]
    next_action: str


@dataclass(frozen=True)
class DecisionEvidencePack:
    review_id: str
    question: str
    asset_id: str
    status: ReadinessStatus
    confidence: Confidence
    evidence_for: list[EvidenceItem]
    evidence_against: list[EvidenceItem]
    missing_evidence: list[EvidenceItem]
    context: list[EvidenceItem]
    similar_cases: list[SimilarCase]
    relationships: list[Relationship]
    ai_summary: AISummary
    next_action: str


@dataclass(frozen=True)
class HumanDecision:
    review_id: str
    actor_id: str
    decision: str
    rationale: str
    decided_at: datetime

