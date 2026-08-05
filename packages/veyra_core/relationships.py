from __future__ import annotations

from datetime import timedelta

from .models import CanonicalEvent, Confidence, Relationship, ReviewRequest


def resolve_relationships(events: list[CanonicalEvent], request: ReviewRequest) -> list[Relationship]:
    relationships: list[Relationship] = []
    by_anchor: dict[tuple[str, str], list[CanonicalEvent]] = {}
    for event in events:
        for key, value in event.anchors.items():
            by_anchor.setdefault((key, value), []).append(event)

    for related in by_anchor.values():
        for left in related:
            for right in related:
                if left.event_id >= right.event_id:
                    continue
                relationships.append(
                    Relationship(
                        from_event_id=left.event_id,
                        to_event_id=right.event_id,
                        relation_type="shared_anchor",
                        reason="Events share an explicit deployment, ticket or mission anchor.",
                    )
                )

    request_window = timedelta(hours=6)
    scoped = [
        event
        for event in events
        if event.asset.asset_id == request.asset_id
        and request.window_start - request_window <= event.occurred_at <= request.window_end + request_window
    ]
    for left in scoped:
        for right in scoped:
            if left.event_id >= right.event_id:
                continue
            relationships.append(
                Relationship(
                    from_event_id=left.event_id,
                    to_event_id=right.event_id,
                    relation_type="same_asset_near_review",
                    reason="Events occurred on the reviewed asset near the decision window.",
                    confidence=Confidence.MEDIUM,
                )
            )
    return dedupe_relationships(relationships)


def dedupe_relationships(items: list[Relationship]) -> list[Relationship]:
    seen: set[tuple[str, str, str]] = set()
    result: list[Relationship] = []
    for item in items:
        key = (item.from_event_id, item.to_event_id, item.relation_type)
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result

