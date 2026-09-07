from datetime import datetime, timezone

import pytest

from nextlaw607.procedure import CriminalCaseState, ProcedureStage


def test_verified_docket_appearance_requires_official_procedure_source_url():
    case = CriminalCaseState("m1", "NY", stage=ProcedureStage.PRETRIAL)
    verified_at = datetime(2026, 9, 7, 16, 0, tzinfo=timezone.utc)

    with pytest.raises(ValueError, match="verified court appearance requires official procedure source URL"):
        case.set_next_appearance(
            datetime(2026, 10, 1, 9, 30, tzinfo=timezone.utc),
            source="court docket entry 51",
            source_kind="docket",
            verified_at=verified_at,
            as_of=verified_at,
        )


def test_stale_verified_appearance_cannot_supersede_newer_verification():
    case = CriminalCaseState("m1", "NY", stage=ProcedureStage.PRETRIAL)
    newer_verification = datetime(2026, 9, 7, 18, 0, tzinfo=timezone.utc)
    older_verification = datetime(2026, 9, 7, 17, 0, tzinfo=timezone.utc)

    case.set_next_appearance(
        datetime(2026, 10, 10, 9, 30, tzinfo=timezone.utc),
        source="counsel confirmation at 18:00 UTC",
        source_kind="counsel_confirmation",
        verified_at=newer_verification,
        as_of=newer_verification,
    )

    with pytest.raises(ValueError, match="stale next-appearance verification cannot supersede newer evidence"):
        case.set_next_appearance(
            datetime(2026, 10, 3, 9, 30, tzinfo=timezone.utc),
            source="earlier counsel confirmation",
            source_kind="counsel_confirmation",
            verified_at=older_verification,
            as_of=newer_verification,
        )
