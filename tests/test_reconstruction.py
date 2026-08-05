import unittest

from packages.veyra_core.ingestion import load_case
from packages.veyra_core.models import ReadinessStatus
from packages.veyra_core.reconstruction import build_decision_pack


class ReconstructionTests(unittest.TestCase):
    def test_case_reconstruction_marks_missing_inspection(self) -> None:
        events, request = load_case("seeds/aceco_like_case.json")
        pack = build_decision_pack(events, request)

        self.assertEqual(pack.status, ReadinessStatus.NOT_READY)
        self.assertTrue(any(item.event_id == "missing:inspection" for item in pack.missing_evidence))
        self.assertTrue(any(item.event_id == "evt_runtime_torque_84392" for item in pack.evidence_against))
        self.assertTrue(pack.relationships)

    def test_similar_cases_become_operational_memory(self) -> None:
        events, request = load_case("seeds/aceco_like_case.json")
        pack = build_decision_pack(events, request)

        summaries = " ".join(case.summary for case in pack.similar_cases).lower()
        self.assertIn("four-hour stoppage", summaries)
        self.assertIn("belt tension", summaries)

    def test_ai_summary_cites_only_selected_evidence(self) -> None:
        events, request = load_case("seeds/aceco_like_case.json")
        pack = build_decision_pack(events, request)

        self.assertTrue(pack.ai_summary.cited_event_ids)
        self.assertIn("inspection", " ".join(pack.ai_summary.uncertainty).lower())
        self.assertIn("Collect", pack.next_action)


if __name__ == "__main__":
    unittest.main()
