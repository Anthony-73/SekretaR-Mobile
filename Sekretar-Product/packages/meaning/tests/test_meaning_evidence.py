import unittest

from sekretar_meaning.enums import EvidenceRole, EvidenceStrength
from sekretar_meaning.value_objects import KnowledgeId, MeaningEvidence, MeaningEvidenceLink


class MeaningEvidenceTests(unittest.TestCase):
    def test_evidence_strength_values_exist(self):
        self.assertEqual(
            {EvidenceStrength.DIRECT, EvidenceStrength.STRONG, EvidenceStrength.WEAK},
            set(EvidenceStrength),
        )

    def test_evidence_link_skeleton(self):
        link = MeaningEvidenceLink(
            evidence=MeaningEvidence(
                strength=EvidenceStrength.STRONG,
                role=EvidenceRole.SUPPORTS,
                summary="Repeated finance mentions across meetings",
            ),
            knowledge_id=KnowledgeId("knowledge-1"),
        )

        self.assertIs(link.evidence.strength, EvidenceStrength.STRONG)
        self.assertIs(link.evidence.role, EvidenceRole.SUPPORTS)


if __name__ == "__main__":
    unittest.main()
