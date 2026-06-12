import unittest

from sekretar_meaning.enums import EntityKind, MeaningEntityValidationState
from sekretar_meaning.value_objects import AccountId, MeaningEntityId


class MeaningEntityTests(unittest.TestCase):
    def test_phase1_entity_kinds_exist(self):
        expected = {EntityKind.PERSON, EntityKind.RESPONSIBILITY_SCOPE}
        self.assertEqual(set(EntityKind), expected)

    def test_entity_skeleton_fields(self):
        from sekretar_meaning.entities import MeaningEntity

        entity = MeaningEntity(
            id=MeaningEntityId("entity-1"),
            account_id=AccountId("account-1"),
            entity_kind=EntityKind.PERSON,
            validation_state=MeaningEntityValidationState.UNVALIDATED,
            display_label="Анна Евгеньевна",
        )

        self.assertIs(entity.entity_kind, EntityKind.PERSON)
        self.assertIs(entity.validation_state, MeaningEntityValidationState.UNVALIDATED)


if __name__ == "__main__":
    unittest.main()
