import pytest

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'ACEest Fitness & Gym' in response.data


def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'ok'


def test_members_endpoint(client):
    response = client.get('/members')
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'members' in json_data
    assert len(json_data['members']) > 0


def test_membership_plan_summary(client):
    response = client.get('/plans')
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'plans' in json_data
    assert json_data['plans'][0]['name'] in {'Basic', 'Premium', 'Elite'}


def test_check_in_endpoint(client):
    response = client.post('/checkin', json={'member_id': 'M101'})
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['member_id'] == 'M101'
    assert json_data['status'] == 'checked_in'


def test_check_in_requires_member_id(client):
    response = client.post('/checkin', json={})
    assert response.status_code == 400
    assert response.get_json()['error'] == 'member_id is required'


def test_check_in_rejects_unknown_member(client):
    response = client.post('/checkin', json={'member_id': 'M999'})
    assert response.status_code == 404
    assert response.get_json()['error'] == 'Member M999 not found'
