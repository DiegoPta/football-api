"""
Implements unit tests to players router.
"""

# Python imports.
from fastapi.testclient import TestClient
from sqlmodel import Session

# Project imports.
import os
from dotenv import load_dotenv
from app.main import app
from app.database.database import engine
from app.models import PlayerDB


load_dotenv('.env')


client = TestClient(app)


def get_token():
    response = client.post('/auth/login', json={"username": os.getenv('USER'), "password": os.getenv('PASSWORD')})
    return response.json()['token']


def delete_created_db_record(model, id):
    session = Session(engine)
    delete_team = session.get(model, id)
    session.delete(delete_team)
    session.commit()
    session.close()


def test_create_player():
    player_to_create = {"firstname": "Name",
                        "lastname": "Lastname",
                        "birthdate": "2000-01-01",
                        "height": 1.80,
                        "nationality": "Colombia",
                        "position": "Midfield",
                        "dorsal": 5,"team_id": 1}
    response = client.post("/players/", json=player_to_create, headers={"Authorization": get_token()})
    json_response = response.json()
    
    id = json_response.pop("id")
    assert response.status_code == 201
    assert json_response == player_to_create
    # delete_created_db_record(PlayerDB, id)


def test_bad_create_player():
    player_to_create = {"firstname": "Name", "lastname": "Lastname", "birthdate": "2000-01-01", "height": 1.80}
    response = client.post("/players/", json=player_to_create, headers={"Authorization": get_token()})
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'Field required'


def test_get_players():
    response = client.get('/players/')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_filtered_players():
    response = client.get('/players/?nationality=jupiter')
    assert response.status_code == 200
    assert response.json() == []


def test_get_player_by_id():
    player_id = client.get('/players/').json()[0]['id']
    response = client.get(f'/players/{player_id}')
    assert response.status_code == 200
    assert response.json()['id'] == player_id
    

def test_bad_get_player_by_id():
    response = client.get('/players/1234241234123451')
    assert response.status_code == 404
    assert response.json() == {"detail": "Player not found"}


def test_update_player():
    player_id = client.get('/players/').json()[0]['id']
    update_data = {"firstname": "Name updated", "lastname": "Lastname updated"}
    response = client.patch(f'/players/{player_id}', json=update_data, headers={"Authorization": get_token()})
    assert response.status_code == 200
    assert response.json()['firstname'] == "Name updated"
    assert response.json()['lastname'] == 'Lastname updated'
    assert response.json()['id'] == player_id


def test_delete_player():
    player_id = client.get('/players/').json()[0]['id']
    response = client.delete(f'/players/{player_id}', headers={"Authorization": get_token()})
    assert response.status_code == 200
    assert response.json()['id'] == player_id
