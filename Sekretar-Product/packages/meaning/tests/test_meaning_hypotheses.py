import unittest

from sekretar_meaning.enums import HypothesisStatus, HypothesisType


class MeaningHypothesisTests(unittest.TestCase):
    def test_phase1_hypothesis_types_exist(self):
        expected = {
            HypothesisType.CO_REFERENCE,
            HypothesisType.ROLE_ATTRIBUTION,
            HypothesisType.RESPONSIBILITY,
            HypothesisType.SPEAKER_IDENTITY,
            HypothesisType.DECISION_INTERPRETATION,
        }
        self.assertEqual(set(HypothesisType), expected)

    def test_hypothesis_status_values_exist(self):
        expected = {
            HypothesisStatus.PROPOSED,
            HypothesisStatus.SUPPORTED,
            HypothesisStatus.CONFIRMED,
            HypothesisStatus.REJECTED,
            HypothesisStatus.SUPERSEDED,
        }
        self.assertEqual(set(HypothesisStatus), expected)


if __name__ == "__main__":
    unittest.main()
