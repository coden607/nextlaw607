from pathlib import Path


def test_cloudflare_live_deployment_workflow_is_release_bound_and_secret_safe() -> None:
    workflow = Path('.github/workflows/cloudflare-live-deploy.yml')
    assert workflow.exists(), 'Cloudflare cannot be promoted without an actual live deployment evidence lane'

    text = workflow.read_text(encoding='utf-8')
    required = (
        'CLOUDFLARE_API_TOKEN',
        'CLOUDFLARE_ACCOUNT_ID',
        'NEXTLAW_API_ORIGIN',
        'wrangler deploy',
        'NEXTLAW_EXACT_REVISION',
        'cloudflare-live-evidence.json',
        'https://',
        'security',
        'rollback',
    )
    for marker in required:
        assert marker in text, f'missing Cloudflare live release marker: {marker}'

    lowered = text.lower()
    assert 'echo ${{ secrets.' not in lowered
    assert 'printenv' not in lowered
    assert 'set -x' not in lowered
