from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

PACKAGE_SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(PACKAGE_SRC))

from sekretar_meaning.entities import MeaningReference  # noqa: E402
from sekretar_meaning.enums import ReferenceKind  # noqa: E402
from sekretar_meaning.value_objects import (  # noqa: E402
    AccountId,
    MeaningReferenceId,
    MeetingRef,
    ReferenceObservation,
    SurfaceForm,
)


def make_meaning_reference(
    *,
    account_id: str = "account-1",
    reference_id: str = "ref-1",
    kind: ReferenceKind = ReferenceKind.PERSON_MENTION,
    surface_form: str = "Анна Евгеньевна",
    meeting_ref: str | None = "meeting-1",
) -> MeaningReference:
    return MeaningReference(
        id=MeaningReferenceId(reference_id),
        account_id=AccountId(account_id),
        observation=ReferenceObservation(
            kind=kind,
            surface_form=SurfaceForm(surface_form),
            meeting_ref=MeetingRef(meeting_ref) if meeting_ref else None,
        ),
    )


def utcnow() -> datetime:
    return datetime.now(timezone.utc)
