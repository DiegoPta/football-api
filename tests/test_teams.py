"""
Implements unit tests to teams router.
"""

# Python imports.
from fastapi.testclient import TestClient
from sqlmodel import Session

# Project imports.
from app.main import app
from app.database.database import engine
from app.models import TeamDB


client = TestClient(app)


def delete_created_db_record(model, id):
    session = Session(engine)
    delete_team = session.get(model, id)
    session.delete(delete_team)
    session.commit()
    session.close()


def test_create_team():
    team_to_create = {"name": "Name", "country": "Country", "city": "City", "stadium": "Stadium", "color": "Color", "coach": "Coach"}
    response = client.post("/teams/", json=team_to_create)
    json_response = response.json()
    delete_created_db_record(TeamDB, json_response.pop("id"))
    assert response.status_code == 201
    assert json_response == team_to_create


def test_bad_create_team():
    team_to_create = {"team_name": "Name", "COUNTRY": "Country", "cities": "City", "manager": "Coach"}
    response = client.post("/teams/", json=team_to_create)
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'Field required'


def test_get_teams():
    response = client.get('/teams/')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_filtered_teams():
    response = client.get('/teams/?stadium=******')
    assert response.status_code == 200
    assert response.json() == []


def test_get_team_by_id():
    team_id = client.get('/teams/').json()[0]['id']
    response = client.get(f'/teams/{team_id}')
    assert response.status_code == 200
    assert response.json()['id'] == team_id
    

def test_bad_get_team_by_id():
    response = client.get('/teams/1234241234123451')
    assert response.status_code == 404
    assert response.json() == {"detail": "Team not found"}


def test_update_team():
    team_id = client.get('/teams/').json()[0]['id']
    update_data = {"city": "London", "color": "Red/White"}
    response = client.patch(f'/teams/{team_id}', json=update_data)
    assert response.status_code == 200
    assert response.json()['city'] == "London"
    assert response.json()['color'] == 'Red/White'
    assert response.json()['id'] == team_id


def test_delete_team():
    team_id = client.get('/teams/').json()[0]['id']
    response = client.delete(f'/teams/{team_id}')
    assert response.status_code == 200
    assert response.json()['id'] == team_id


def test_get_players_by_team_id():
    team_id = client.get('/teams/').json()[0]['id']
    response = client.get(f'/teams/{team_id}/players')
    assert response.status_code == 200
    assert isinstance(response.json(), list)
