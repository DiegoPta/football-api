"""
Implements the players operations on the database.
"""

# Python imports.
from sqlmodel import Session, select

# Project imports.
from ...models import PlayerBase, Player, PlayerDB, PlayerUpdates


def create_player(db: Session, player: PlayerBase) -> Player:
    """
    Creates a new player in the database.
    @param db:      Database session.
    @param player:  PlayerBase object to be added into the database.
    @return:        Player object created into the database.
    """
    db_player = PlayerDB(**player.model_dump())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


def get_player_by_id(db: Session, player_id: int) -> Player:
    """
    Gets a player by ID.
    @param db:          Database session.
    @param player_id:   Identifier of the player.
    @return:            Player by the given id.
    """
    return db.exec(select(PlayerDB).where(PlayerDB.id == player_id).where(PlayerDB.is_active == True)).first()


def get_players(db: Session, filters: dict) -> list[Player]:
    """
    Gets a list with all players availables and filtered by one or more parameters.
    @param db:      Database session.
    @param filters: Dictionary with filters to search players.
    @return:        List of players.
    """    
    query = select(PlayerDB).where(PlayerDB.is_active == True)

    for field, value in filters.items():
        if value:
            query = query.where(getattr(PlayerDB, field).contains(value))

    return db.exec(query).all()


def update_player(db: Session, player_id: int, player_updates: PlayerUpdates) -> Player:
    """
    Gets a list with all teams availables or filtered by one parameter.
    @param db:              Database session.
    @param player_id:       Identifier of the player.
    @param player_updates:  Object with fields and data to update.
    @return:                Updated player by the given id.
    """
    if player := get_player_by_id(db, player_id):
        update_data = player_updates.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(player, key, value)
        
        db.commit()
        db.refresh(player)
        
        return player
    

def delete_player(db: Session, player_id: int) -> Player:
    """
    Deletes (inactivates) a player by ID.
    @param db:      Database session.
    @param player_id: Identifier of the player.
    """
    if player := get_player_by_id(db, player_id):
        player.is_active = False
        db.commit()
        db.refresh(player)
        return player
    