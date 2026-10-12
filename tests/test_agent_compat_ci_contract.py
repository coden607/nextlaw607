from pathlib import Path


def test_ci_has_real_agent_framework_compatibility_lane():
    workflow = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")

    assert "agent-framework-compat" in workflow
    assert "pip install -e '.[agents]'" in workflow or 'pip install -e ".[agents]"' in workflow
    assert "compat/test_agent_frameworks.py" in workflow
