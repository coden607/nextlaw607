import json
from datetime import date
from urllib.parse import parse_qs, urlparse

from nextlaw607.ny_openleg import NYOpenLegClient


def test_historical_section_uses_official_snapshot_and_strips_key_from_provenance():
    seen = {}
    payload = {
        "success": True,
        "result": {
            "lawVersion": {"lawId": "CPL", "activeDate": "2026-08-01"},
            "documents": {
                "lawId": "CPL",
                "locationId": "-ROOT",
                "documents": {
                    "items": [
                        {
                            "lawId": "CPL",
                            "locationId": "140.50",
                            "title": "Search warrants; application",
                            "activeDate": "2026-08-01",
                            "repealed": False,
                            "text": "Official section text",
                            "documents": {"items": []},
                        }
                    ]
                },
            },
        },
    }

    def transport(request):
        seen["url"] = request.full_url
        return 200, json.dumps(payload).encode()

    client = NYOpenLegClient("secret-key", transport=transport)
    section = client.fetch_section("CPL", "140.50", on_date=date(2026, 9, 1))

    parsed = urlparse(seen["url"])
    query = parse_qs(parsed.query)
    assert query["key"] == ["secret-key"]
    assert query["date"] == ["2026-09-01"]
    assert query["full"] == ["true"]
    assert section.text == "Official section text"
    assert section.active_date == date(2026, 8, 1)
    assert "secret-key" not in section.source_url
    assert section.source_url.startswith("https://legislation.nysenate.gov/api/3/laws/CPL")


def test_missing_section_fails_closed():
    payload = {"success": True, "result": {"documents": {"locationId": "root", "documents": {"items": []}}}}
    client = NYOpenLegClient("k", transport=lambda request: (200, json.dumps(payload).encode()))
    try:
        client.fetch_section("CPL", "999", on_date=date(2026, 9, 1))
    except LookupError as exc:
        assert "999" in str(exc)
    else:
        raise AssertionError("missing official section must not return fabricated text")
