import unittest

from conftest import make_meaning_reference
from sekretar_meaning.enums import ReferenceKind


class MeaningReferenceTests(unittest.TestCase):
    def test_phase1_reference_kinds_exist(self):
        expected = {
            ReferenceKind.PERSON_MENTION,
            ReferenceKind.ROLE_MENTION,
            ReferenceKind.RESPONSIBILITY_MENTION,
            ReferenceKind.SPEAKER_REF,
            ReferenceKind.GROUP_MENTION,
        }
        self.assertEqual(set(ReferenceKind), expected)

    def test_reference_skeleton_is_observational(self):
        reference = make_meaning_reference(kind=ReferenceKind.PERSON_MENTION)

        self.assertIs(reference.observation.kind, ReferenceKind.PERSON_MENTION)
        self.assertEqual(reference.observation.surface_form.value, "Анна Евгеньевна")


if __name__ == "__main__":
    unittest.main()
