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
