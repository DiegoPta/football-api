"""
Implements the teams operations on the database.
"""

# Python imports.
from sqlmodel import Session, select

# Project imports.
from ...models import TeamBase, Team, TeamDB, TeamUpdates


def create_team(db: Session, team: TeamBase) -> Team:
    """
    Creates a new team in the database.
    @param db:      Database session.
    @param team:    TeamBase object to be added into the database.
    @return:        Team object created into the database.
    """
    db_team = TeamDB(**team.model_dump())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


def get_team_by_id(db: Session, team_id: int) -> Team:
    """
    Gets a team by ID.
    @param db:      Database session.
    @param team_id: Identifier of the team.
    @return:        Team by the given id.
    """
    return db.exec(select(TeamDB).where(TeamDB.id == team_id).where(TeamDB.is_active == True)).first()


def get_teams(db: Session, filters: dict) -> list[Team]:
    """
    Gets a list with all teams availables and filtered by one or more parameters.
    @param db:      Database session.
    @param filters: Dictionary with filters to search teams.
    @return:        List of teams.
    """    
    query = select(TeamDB).where(TeamDB.is_active == True)

    for field, value in filters.items():
        if value:
            query = query.where(getattr(TeamDB, field).contains(value))

    return db.exec(query).all()


def update_team(db: Session, team_id: int, team_updates: TeamUpdates) -> Team:
    """
    Gets a list with all teams availables or filtered by one parameter.
    @param db:              Database session.
    @param team_id:         Identifier of the team.
    @param team_updates:    Object with fields and data to update.
    @return:                Updated team by the given id.
    """
    if team := get_team_by_id(db, team_id):
        update_data = team_updates.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(team, key, value)
        
        db.commit()
        db.refresh(team)
        
        return team
    

def delete_team(db: Session, team_id: int) -> Team:
    """
    Deletes (inactivates) a team by ID.
    @param db:      Database session.
    @param team_id: Identifier of the team.
    """
    if team := get_team_by_id(db, team_id):
        team.is_active = False
        db.commit()
        db.refresh(team)
        return team
    