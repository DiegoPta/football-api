"""
Main script that runs the application.
"""

# Python imports.
from fastapi import FastAPI

# Project imports.
from .routers import teams
from .database.database import create_db_and_tables


app = FastAPI()


app.include_router(teams.router)


@app.on_event("startup")
def on_startup():
    """
    Creates the database and their tables based on the models.
    This runs when the server is up.
    """
    create_db_and_tables()
