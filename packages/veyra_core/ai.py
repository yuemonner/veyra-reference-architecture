from __future__ import annotations

from .models import AISummary, EvidenceItem


def bounded_summary(
    question: str,
    evidence_for: list[EvidenceItem],
    evidence_against: list[EvidenceItem],
    missing_evidence: list[EvidenceItem],
) -> AISummary:
    cited = [item.event_id for item in evidence_for[:2] + evidence_against[:3]]
    if missing_evidence:
        answer = "The review is not decision-complete because required evidence is missing."
        next_action = f"Collect {missing_evidence[0].label.lower()} before expanding the system."
    elif evidence_against:
        answer = "The system may proceed only through a limited test because recent evidence raises operational risk."
        next_action = "Run a limited monitored deployment and record the outcome."
    else:
        answer = "The selected evidence supports proceeding."
        next_action = "Proceed and attach the decision outcome to operational memory."
    return AISummary(
        answer=answer,
        cited_event_ids=cited,
        uncertainty=[item.label for item in missing_evidence],
        next_action=next_action,
    )

