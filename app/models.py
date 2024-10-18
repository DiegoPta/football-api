"""
Script defining the Pydantic (SQLModel) and database models.
"""

# Python imports.
from sqlmodel import SQLModel, Field, Relationship
from datetime import date


class TeamBase(SQLModel):
    name: str = Field(index=True, max_length=30)
    country: str = Field(index=True, max_length=20)
    city: str = Field(index=True, max_length=20)
    stadium: str = Field(max_length=20)
    color: str = Field(max_length=20)
    coach: str = Field(max_length=30)


class Team(TeamBase):
    id: int
    players: list['Player']


class TeamDB(TeamBase, table=True):
    __tablename__ = 'teams'
    id: int | None = Field(default=None, primary_key=True)
    players: list['Player'] = Relationship(back_populates='team')


class PlayerBase(SQLModel):
    firstname: str = Field(index=True, min_length=2, max_length=30)
    lastname: str = Field(index=True, min_length=5, max_length=30)
    birthdate: date = Field()
    height: float = Field(max_digits=3)
    nationality: str = Field(max_length=30)
    position: str = Field(max_length=20)
    dorsal: int = Field(max_digits=2)


class Player(PlayerBase):
    id: int
    team_id: int


class PlayerDB(PlayerBase, table=True):
    __tablename__ = 'players'
    id: int | None = Field(default=None, primary_key=True)
    team_id: int = Field(default=None, foreign_key='teams.id')
    team: Team = Relationship(back_populates='players')