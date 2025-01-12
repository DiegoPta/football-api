"""
Implements the router in charge of player management.
"""

# Python imports.
from sqlmodel import Session
from fastapi import APIRouter, Depends, Body, Path, Query, Security, status, HTTPException

# Project imports.
from .auth import verify_token_dependency
from ..database.database import get_session
from ..database.operations import players as db_players
from ..models import Player, PlayerBase, PlayerUpdates


router = APIRouter(prefix='/players', tags=['Players'])


@router.post('/', status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_token_dependency)])
def create_player(player_data: PlayerBase = Body(), db_session: Session = Depends(get_session)) -> Player:
    """
    Creates a new player in the database.
    - **player_data**:  Player object to be added into the database.
    """
    return db_players.create_player(db_session, player_data)


@router.get('/{player_id}/', status_code=status.HTTP_200_OK)
def get_player_by_id(player_id: int = Path(), db_session: Session = Depends(get_session)) -> Player:
    """
    Gets a player by ID.
    - **player_id**:    Identifier of the player.
    """
    if player := db_players.get_player_by_id(db_session, player_id):
        return player
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")


@router.get('/', status_code=status.HTTP_200_OK)
def get_players(db_session: Session = Depends(get_session),
                firstname: str = Query(default=None),
                lastname: str = Query(default=None),
                nationality: str = Query(default=None),
                position: str = Query(default=None)) -> list[Player]:
    """
    Gets a list with all players availables or filtered by one parameter.
    - **firstname**:    Player firstname to filter.
    - **lastname**:     Player lastname to filter.
    - **nationality**:  Player nationality to filter.
    - **position**:     Player position to filter.
    """
    filters = {"firstname": firstname, "lastname": lastname, "nationality": nationality, "position": position}
    players = db_players.get_players(db_session, filters)
    if players or players == []:
        return players
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Failed request')


@router.patch('/{player_id}/', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_token_dependency)])
def update_player(player_id: int = Path(), player_updates: PlayerUpdates = Body(), db_session: Session = Depends(get_session)) -> Player:
    """
    Updates a player by id.
    - **player_id**:        Identifier of the player.
    - **player_updates**:   Object with fields and data to update.
    """
    if player := db_players.update_player(db_session, player_id, player_updates):
        return player
    raise HTTPException(status_code=404, detail="Player not found")
    

@router.delete('/{player_id}/', status_code=status.HTTP_200_OK, dependencies=[Security(verify_token_dependency)])
def delete_player(player_id: int = Path(), db_session: Session = Depends(get_session)) -> Player:
    """
    Deletes (inactivates) a player by ID.
    - **player_id**:    Identifier of the player.
    """
    if player := db_players.delete_player(db_session, player_id):
        return player
    raise HTTPException(status_code=404, detail="Player not found")
