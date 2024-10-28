"""
Implements the router in charge of team management.
"""

# Python imports.
from fastapi import APIRouter, Depends, Body, Path, Query, status, HTTPException
from sqlmodel import Session

# Project imports.
from ..database.database import get_session
from ..database.operations import teams as db_teams
from ..models import TeamBase, Team, TeamUpdates, Player



router = APIRouter(prefix='/teams', tags=['Teams'])


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_team(team_data: TeamBase = Body(), db_session: Session = Depends(get_session)) -> Team:
    """
    Creates a new team in the database.
    - **team_data**:    Team object to be added into the database.
    """
    return db_teams.create_team(db_session, team_data)


@router.get('/{team_id}/', status_code=status.HTTP_200_OK)
def get_team_by_id(team_id: int = Path(), db_session: Session = Depends(get_session)) -> Team:
    """
    Gets a team by ID.
    - **team_id**:     Identifier of the team.
    """
    if team := db_teams.get_team_by_id(db_session, team_id):
        return team
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")


@router.get('/', status_code=status.HTTP_200_OK)
def get_teams(db_session: Session = Depends(get_session),
              name: str = Query(default=None),
              country: str = Query(default=None),
              city: str = Query(default=None),
              stadium: str = Query(default=None),
              color: str = Query(default=None),
              coach: str = Query(default=None)) -> list[Team]:
    """
    Gets a list with all teams availables or filtered by one parameter.
    - **name**:        Team name to filter.
    - **country**:     Team country to filter.
    - **city**:        Team city to filter.
    - **stadium**:     Team stadium to filter.
    - **color**:       Team color to filter.
    - **coach**:       Team coach to filter.
    """
    filters = {"name": name, "country": country, "city": city, "stadium": stadium, "color": color, "coach": coach}
    teams = db_teams.get_teams(db_session, filters)
    if teams or teams == []:
        return teams
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Failed request')


@router.get('/{team_id}/players/', status_code=status.HTTP_200_OK)
def get_players_by_team_id(team_id: int = Path(), db_session: Session = Depends(get_session)) -> list[Player]:
    """
    Gets team's players by team ID.
    - **team_id**:     Identifier of the team.
    """
    if team := db_teams.get_team_by_id(db_session, team_id):
        return team.players
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")


@router.patch('/{team_id}/', status_code=status.HTTP_200_OK)
def update_team(team_id: int = Path(), team_updates: TeamUpdates = Body(), db_session: Session = Depends(get_session)) -> Team:
    """
    Updates a team by id.
    - **team_id**:      Identifier of the team.
    - **team_updates**: Object with fields and data to update.
    """
    if team := db_teams.update_team(db_session, team_id, team_updates):
        return team
    raise HTTPException(status_code=404, detail="Team not found")
    

@router.delete('/{team_id}/', status_code=status.HTTP_200_OK)
def delete_team(team_id: int = Path(), db_session: Session = Depends(get_session)) -> Team:
    """
    Deletes (inactivates) a team by ID.
    - **team_id**:     Identifier of the team.
    """
    if team := db_teams.delete_team(db_session, team_id):
        return team
    raise HTTPException(status_code=404, detail="Team not found")
