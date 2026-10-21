from nextlaw607.features.ny_issue_classifier import classify

def test_classifier_is_deterministic_and_multi_label():
    assert classify("CPL 245 discovery and 30.30 readiness") == ("discovery", "speedy_trial")

def test_classifier_has_safe_fallbacks():
    assert classify("") == ("unknown",)
    assert classify("criminal procedure question") == ("general_criminal",)
