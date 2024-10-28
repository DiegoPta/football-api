"""
Script defining the Pydantic (SQLModel) and database models to Team.
"""

# Python imports.
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import MetaData
from datetime import date


metadata = MetaData()


class TeamBase(SQLModel):
    name: str = Field(index=True, max_length=30)
    country: str = Field(index=True, max_length=20)
    city: str = Field(index=True, max_length=20)
    stadium: str = Field(max_length=30)
    color: str = Field(max_length=20)
    coach: str = Field(max_length=30) 


class TeamUpdates(TeamBase):
    name: str = None
    country: str = None
    city: str = None
    stadium: str = None
    color: str = None
    coach: str = None


class Team(TeamBase):
    id: int


class TeamDB(TeamBase, table=True, metadata=metadata):
    __tablename__ = 'teams'
    id: int | None = Field(default=None, primary_key=True)
    is_active: bool = Field(default=True)
    players: list['PlayerDB'] = Relationship(back_populates='team')


class PlayerBase(SQLModel):
    firstname: str = Field(index=True, min_length=2, max_length=30)
    lastname: str = Field(index=True, min_length=5, max_length=30)
    birthdate: date = Field()
    height: float = Field()
    nationality: str = Field(max_length=30)
    position: str = Field(max_length=20)
    dorsal: int = Field()
    team_id: int = Field()


class PlayerUpdates(PlayerBase):
    firstname: str = None
    lastname: str = None
    birthdate: date = None
    height: float = None
    nationality: str = None
    position: str = None
    dorsal: int = None
    team_id: int = None


class Player(PlayerBase):
    id: int
    is_active: bool


class PlayerDB(PlayerBase, table=True, metadata=metadata):
    __tablename__ = 'players'
    id: int | None = Field(default=None, primary_key=True)
    is_active: bool = Field(default=True)
    team_id: int = Field(default=None, foreign_key='teams.id')
    team: TeamDB = Relationship(back_populates='players')