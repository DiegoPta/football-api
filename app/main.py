"""
Main script that runs the application.
"""

# Python imports.
from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager


# Project imports.
from .routers import auth, teams, players
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


@app.get('/', status_code=status.HTTP_200_OK, include_in_schema=False)
def root() -> dict:
    """
    Root endpoint.
    """
    return RedirectResponse(url='/docs')


app.include_router(auth.router)
app.include_router(teams.router)
app.include_router(players.router)
