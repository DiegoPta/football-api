"""
Implements the router in charge of team management.
"""

# Python imports.
from fastapi import APIRouter, Depends, Body, Path, Query, status, HTTPException
from sqlmodel import Session, select

# Project imports.
from ..database import get_session
from ..models import Team, TeamDB, TeamBase, TeamUpdates, Player


router = APIRouter(prefix='/teams', tags=['Teams'])


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_team(team: TeamBase = Body(), db_session: Session = Depends(get_session)) -> Team:
    """
    Creates a new team in the database.
    - **team**:    Team object to be added into the database.
    """
    db_team = TeamDB(**team.model_dump())
    db_session.add(db_team)
    db_session.commit()
    db_session.refresh(db_team)
    return db_team


@router.get('/{team_id}/', status_code=status.HTTP_200_OK)
def get_team_by_id(team_id: int = Path(), db_session: Session = Depends(get_session)) -> Team:
    """
    Gets a team by ID.
    - **team_id**:     Identifier of the team.
    """
    if team_db := db_session.exec(select(TeamDB).where(TeamDB.id == team_id).where(TeamDB.is_active == True)).first():
        return team_db
    raise HTTPException(status_code=404, detail="Team not found")


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
    filters = {"name": name,
               "country": country,
               "city": city,
               "stadium": stadium,
               "color": color,
               "coach": coach}
    
    query = select(TeamDB).where(TeamDB.is_active == True)

    # if name: query = query.where(TeamDB.name.contains(name))
    # if country: query = query.where(TeamDB.country.contains(country))
    # if city: query = query.where(TeamDB.city.contains(city))
    # if stadium: query = query.where(TeamDB.stadium.contains(stadium))
    # if color: query = query.where(TeamDB.color.contains(color))
    # if coach: query = query.where(TeamDB.coach.contains(coach))

    for field, value in filters.items():
        if value:
            query = query.where(getattr(TeamDB, field).contains(value))

    return db_session.exec(query).all()


@router.get('/{team_id}/players/', status_code=status.HTTP_200_OK)
def get_players_by_team_id(team_id: int = Path(), db_session: Session = Depends(get_session)) -> list[Player]:
    """
    Gets team's players by team ID.
    - **team_id**:     Identifier of the team.
    """
    if team_db := db_session.exec(select(TeamDB).where(TeamDB.id == team_id).where(TeamDB.is_active == True)).first():
        return team_db.players
    raise HTTPException(status_code=404, detail="Team not found")


@router.patch('/{team_id}/', status_code=status.HTTP_200_OK)
def update_team(team_id: int = Path(), team_updates: TeamUpdates = Body(), db_session: Session = Depends(get_session)) -> Team:
    """
    Gets a list with all teams availables or filtered by one parameter.
    - **name**:        Team name to update.
    - **country**:     Team country to update.
    - **city**:        Team city to update.
    - **stadium**:     Team stadium to update.
    - **color**:       Team color to update.
    - **coach**:       Team coach to update.
    """
    if team_db := db_session.exec(select(TeamDB).where(TeamDB.id == team_id).where(TeamDB.is_active == True)).first():
        update_data = team_updates.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(team_db, key, value)
        
        db_session.commit()
        db_session.refresh(team_db)
        
        return team_db
    raise HTTPException(status_code=404, detail="Team not found")
    

@router.delete('/{team_id}/', status_code=status.HTTP_200_OK)
def delete_team(team_id: int = Path(), db_session: Session = Depends(get_session)) -> Team:
    """
    Deletes (inactivates) a team by ID.
    - **team_id**:     Identifier of the team.
    """
    if team_db := db_session.exec(select(TeamDB).where(TeamDB.id == team_id).where(TeamDB.is_active == True)).first():
        team_db.is_active = False
        db_session.commit()
        db_session.refresh(team_db)
        return team_db
    raise HTTPException(status_code=404, detail="Team not found")