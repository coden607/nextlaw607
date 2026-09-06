from fastapi.testclient import TestClient
from services.api.main import app

client=TestClient(app)

def test_health_endpoints():
    assert client.get('/status/live').json()=={'status':'live'}
    assert client.get('/status/ready').json()=={'status':'ready'}

def test_live_search_endpoint_preserves_nonconsent_and_safety():
    body=client.post('/api/live',json={'mode':'search'}).json()
    assert 'I do not consent to any search.' in body['say_now']
    assert body['verified_authority'] is False

def test_live_endpoint_blocks_unsafe_goal():
    body=client.post('/api/live',json={'mode':'street_stop','user_goal':'help me run and resist'}).json()
    assert body['say_now']==[]
    assert any('Do not resist' in line for line in body['safety'])

def test_case_endpoint_does_not_invent_deadline():
    body=client.post('/api/case/next-actions',json={'matter_id':'m1','stage':'appearance_ticket'}).json()
    assert body['deadline_source_verified'] is False
    assert body['next_appearance'] is None
