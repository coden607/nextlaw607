import json
from nextlaw607.authority import CitationFirewall, AuthorityStatus
from nextlaw607.courtlistener import CourtListenerClient, COURTLISTENER_MCP_URL


def transport(request):
    payload={"results":[{"cluster_id":6613686,"caseName":"Foo v. Foo","caseNameFull":"Foo v. Foo","citation":["101 Haw. 235"],"court":"Hawaii Intermediate Court of Appeals","court_id":"hawapp","dateFiled":"2003-01-10","absolute_url":"/opinion/6613686/foo-v-foo/","status":"Published"}]}
    assert "/api/rest/v4/search/" in request.full_url
    assert "type=o" in request.full_url
    return 200, json.dumps(payload).encode()


def test_current_mcp_endpoint_is_recorded(): assert COURTLISTENER_MCP_URL == "https://mcp.courtlistener.com/"
def test_search_parses_v4_opinion_hit():
    hit=CourtListenerClient(transport=transport).search_opinions("foo")[0]
    assert hit.cluster_id==6613686
    assert hit.citations==("101 Haw. 235",)
    assert hit.canonical_url.endswith('/opinion/6613686/foo-v-foo/')
def test_search_candidate_is_not_auto_declared_good_law():
    client=CourtListenerClient(transport=transport)
    candidate=client.candidate_authority(client.search_opinions('foo')[0],jurisdiction='HI',holding='candidate holding')
    assert candidate.status is AuthorityStatus.UNKNOWN
    assert not CitationFirewall().verify(candidate).verified
def test_token_is_sent_only_when_configured():
    seen=[]
    def t(req):
        seen.append(req.get_header('Authorization')); return 200, b'{"results":[]}'
    CourtListenerClient(token='abc',transport=t).search_opinions('x')
    assert seen==['Token abc']
