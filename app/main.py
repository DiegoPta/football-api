"""
Main script that runs the application.
"""

# Python imports.
from fastapi import FastAPI
from contextlib import asynccontextmanager

# Project imports.
from .routers import teams
from .database.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Creates the database and their tables based on the models.
    This runs when the server is up.
    """
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(teams.router)
