import re
from pathlib import Path


def test_cloudflare_live_deployment_workflow_is_release_bound_and_secret_safe() -> None:
    workflow = Path('.github/workflows/cloudflare-live-deploy.yml')
    assert workflow.exists(), 'Cloudflare cannot be promoted without an actual live deployment evidence lane'

    text = workflow.read_text(encoding='utf-8')
    required = (
        'CLOUDFLARE_API_TOKEN',
        'CLOUDFLARE_ACCOUNT_ID',
        'NEXTLAW_API_ORIGIN',
        'NEXTLAW_EXACT_REVISION',
        'cloudflare-live-evidence.json',
        'https://',
        'security',
        'rollback',
    )
    for marker in required:
        assert marker in text, f'missing Cloudflare live release marker: {marker}'

    assert re.search(r'wrangler(?:@\d+(?:\.\d+){2})?\s+deploy\b', text), (
        'Cloudflare live release lane must execute Wrangler deploy; an explicitly pinned Wrangler version is allowed'
    )

    lowered = text.lower()
    assert 'echo ${{ secrets.' not in lowered
    assert 'printenv' not in lowered
    assert 'set -x' not in lowered
