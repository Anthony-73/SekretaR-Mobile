import unittest

from sekretar_meaning.enums import MeaningDecisionState, MeaningEntityValidationState


class DecisionScopeTests(unittest.TestCase):
    def test_decision_state_values_exist(self):
        expected = {
            MeaningDecisionState.RESOLVED,
            MeaningDecisionState.UNRESOLVED,
            MeaningDecisionState.CONFLICTED,
        }
        self.assertEqual(set(MeaningDecisionState), expected)

    def test_validation_state_values_exist(self):
        expected = {
            MeaningEntityValidationState.NOT_APPLICABLE,
            MeaningEntityValidationState.UNVALIDATED,
            MeaningEntityValidationState.VALIDATED,
            MeaningEntityValidationState.CORRECTED,
            MeaningEntityValidationState.CONTRADICTED,
        }
        self.assertEqual(set(MeaningEntityValidationState), expected)


if __name__ == "__main__":
    unittest.main()
