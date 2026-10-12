from datetime import date, timedelta
import pytest
from nextlaw607.encounter import EncounterMode
from nextlaw607.live import LiveEncounterEngine
from nextlaw607.rules import LegalRule, RuleRegistry, RuleSourceKind
from nextlaw607.evals import LegalEvalRunner


def rule(**kw):
    base=dict(id='r1',jurisdiction='NY',topic='test',statement='Verified rule',source_url='https://official.example/rule',source_kind=RuleSourceKind.OFFICIAL,verified_on=date.today(),effective_from=date(2025,1,1))
    base.update(kw); return LegalRule(**base)

def test_rule_registry_requires_jurisdiction_date_and_freshness():
    registry=RuleRegistry([rule()])
    assert registry.require(topic='test',jurisdiction='NY',on_date=date(2026,1,1))[0].id=='r1'
    with pytest.raises(LookupError): registry.require(topic='test',jurisdiction='PA',on_date=date(2026,1,1))
    with pytest.raises(LookupError): registry.require(topic='test',jurisdiction='NY',on_date=date(2024,1,1))

def test_stale_rule_is_not_applicable():
    registry=RuleRegistry([rule(verified_on=date.today()-timedelta(days=100))],max_verification_age_days=90)
    assert registry.applicable(topic='test',jurisdiction='NY',on_date=date.today())==()

def test_live_adversarial_eval_corpus_passes():
    runner=LegalEvalRunner(); cases=runner.load('evals/live_safety.json'); engine=LiveEncounterEngine()
    def execute(data):
        r=engine.respond(EncounterMode(data['mode']),user_goal=data.get('user_goal','protect my rights'))
        return ' '.join(r.say_now+r.safety+r.preserve_for_later)
    report=runner.run(cases,execute)
    assert report.passed, report.results
    assert report.pass_rate==1.0

def test_suppression_adversarial_eval_corpus_passes():
    from nextlaw607.suppression import SuppressionAnalyzer, SuppressionFacts
    runner = LegalEvalRunner()
    cases = runner.load('evals/suppression_issues.json')
    analyzer = SuppressionAnalyzer()
    def execute(data):
        issues = analyzer.analyze(SuppressionFacts(**data))
        return ' '.join(f'{issue.code} {issue.summary}' for issue in issues)
    report = runner.run(cases, execute)
    assert report.passed, report.results
    assert report.pass_rate == 1.0
