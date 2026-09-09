from datetime import datetime, timezone

import pytest

from nextlaw607.procedure import CriminalCaseState, DeadlineKind, ProcedureStage


def test_verified_court_deadline_requires_official_procedure_source_url():
    case = CriminalCaseState("m1", "NY", stage=ProcedureStage.MOTIONS)

    with pytest.raises(ValueError, match="official procedure source URL"):
        case.add_deadline(
            "motion filing",
            datetime(2026, 10, 15, 17, 0, tzinfo=timezone.utc),
            source="court scheduling order dated 2026-09-25",
            source_kind="court_notice",
            kind=DeadlineKind.MOTION,
            verified_at=datetime(2026, 9, 25, 12, 0, tzinfo=timezone.utc),
            as_of=datetime(2026, 9, 26, 12, 0, tzinfo=timezone.utc),
        )
