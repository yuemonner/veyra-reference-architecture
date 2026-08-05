from __future__ import annotations

from .ai import bounded_summary
from .models import (
    CanonicalEvent,
    Confidence,
    DecisionEvidencePack,
    EvidenceItem,
    EvidenceRole,
    ReadinessStatus,
    ReviewRequest,
    SimilarCase,
)
from .relationships import resolve_relationships


def build_decision_pack(events: list[CanonicalEvent], request: ReviewRequest) -> DecisionEvidencePack:
    scoped = _scoped_events(events, request)
    relationships = resolve_relationships(scoped, request)
    evidence_for = [_evidence_item(event, "Supports proceeding") for event in scoped if event.evidence_role == EvidenceRole.FOR]
    evidence_against = [
        _evidence_item(event, "Raises risk for this decision")
        for event in scoped
        if event.evidence_role == EvidenceRole.AGAINST
    ]
    context = [
        _evidence_item(event, "Relevant operational context")
        for event in scoped
        if event.evidence_role in (EvidenceRole.CONTEXT, EvidenceRole.UNKNOWN)
    ]
    missing_evidence = _missing_evidence(scoped, request)
    similar_cases = _similar_cases(events, request)
    status, confidence = _classify(evidence_for, evidence_against, missing_evidence)
    summary = bounded_summary(request.question, evidence_for, evidence_against, missing_evidence)
    return DecisionEvidencePack(
        review_id=request.review_id,
        question=request.question,
        asset_id=request.asset_id,
        status=status,
        confidence=confidence,
        evidence_for=evidence_for,
        evidence_against=evidence_against,
        missing_evidence=missing_evidence,
        context=context,
        similar_cases=similar_cases,
        relationships=relationships,
        ai_summary=summary,
        next_action=summary.next_action,
    )


def _scoped_events(events: list[CanonicalEvent], request: ReviewRequest) -> list[CanonicalEvent]:
    scoped: list[CanonicalEvent] = []
    for event in events:
        if event.asset.asset_id != request.asset_id:
            continue
        explicit_anchor = bool(set(event.anchors.items()) & set(request.anchors.items()))
        in_window = request.window_start <= event.occurred_at <= request.window_end
        historical_context = event.event_type in {"maintenance", "outcome"} and event.occurred_at < request.window_start
        if explicit_anchor or in_window or historical_context:
            scoped.append(event)
    return sorted(scoped, key=lambda event: event.sortable_key)


def _evidence_item(event: CanonicalEvent, reason: str) -> EvidenceItem:
    return EvidenceItem(
        event_id=event.event_id,
        label=event.event_type.replace("_", " ").title(),
        role=event.evidence_role,
        occurred_at=event.occurred_at,
        source_system=event.source.system,
        summary=event.summary,
        reason=reason,
    )


def _missing_evidence(scoped: list[CanonicalEvent], request: ReviewRequest) -> list[EvidenceItem]:
    present = {event.event_type for event in scoped}
    missing: list[EvidenceItem] = []
    for required in request.required_evidence:
        if required in present:
            continue
        missing.append(
            EvidenceItem(
                event_id=f"missing:{required}",
                label=required.replace("_", " ").title(),
                role=EvidenceRole.MISSING,
                occurred_at=None,
                source_system="required_evidence",
                summary=f"No {required.replace('_', ' ')} was found in the review scope.",
                reason="Required before this decision can be treated as complete.",
            )
        )
    return missing


def _similar_cases(events: list[CanonicalEvent], request: ReviewRequest) -> list[SimilarCase]:
    current_keywords = {"torque", "variance", "belt", "drive", "stoppage"}
    cases: list[SimilarCase] = []
    for event in sorted(events, key=lambda item: item.occurred_at, reverse=True):
        if event.asset.asset_id != request.asset_id or event.occurred_at >= request.window_start:
            continue
        text = event.summary.lower()
        if any(keyword in text for keyword in current_keywords):
            cases.append(
                SimilarCase(
                    event_id=event.event_id,
                    occurred_at=event.occurred_at,
                    summary=event.summary,
                    outcome=event.measurements.get("outcome"),
                    reason="Historical event shares operational signature with the current review.",
                )
            )
        if len(cases) == 3:
            break
    return list(reversed(cases))


def _classify(
    evidence_for: list[EvidenceItem],
    evidence_against: list[EvidenceItem],
    missing_evidence: list[EvidenceItem],
) -> tuple[ReadinessStatus, Confidence]:
    if missing_evidence:
        return ReadinessStatus.NOT_READY, Confidence.LOW
    if evidence_against and evidence_for:
        return ReadinessStatus.READY_FOR_LIMITED_TEST, Confidence.MEDIUM
    if evidence_against:
        return ReadinessStatus.NEEDS_REVIEW, Confidence.LOW
    return ReadinessStatus.READY, Confidence.HIGH

