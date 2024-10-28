# Football API

## Project Overview
This project is a RESTful API for managing football players and teams, built using FastAPI. The API supports CRUD operations for players and teams, allowing users to create, read, update, and delete records in a SQLite database.


## Features
- Players CRUD: Create, read, update, and delete football players.
- Teams CRUD: Create, read, update, and delete football teams.
- Relationships: Define relationships between players and teams (one-to-many).


## Technologies Used
1. FastAPI: A modern, fast (high-performance), web framework for building APIs with Python.
2. SQLModel: An ORM and data validation library that unifies Pydantic and SQLAlchemy.
3. Uvicorn: An ASGI server for serving FastAPI applications.
4. SQLite: A lightweight database used for local development.


## Setup and Installation

### 1. Clone the repository
git clone https://gitlab.com/yourusername/football-api.git
cd football-api

### 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`

### 3. Install the dependencies
pip install -r requirements.txt

### 4. Run the application
uvicorn app.main:app --reload

### 5. Access the API documentation
Open your browser and navigate to http://127.0.0.1:8000/docs to view the automatically generated API documentation.


## Project structure
### football-api/
#### ├── alembic/
#### ├── app/
#### │   ├── database/
#### │   |   ├── operations/
#### │   |   |   ├── __init__.py
#### |   |   |   ├── players.py
#### │   |   |   └── teams.py
#### │   |   └── database.py
#### │   |── routers/
#### │   |   ├── __init__.py
#### │   |   ├── players.py
#### │   |   └── teams.py
#### │   ├── __init__.py
#### │   ├── main.py
#### │   └── models.py
#### ├── tests/
#### │   ├── __init__.py
#### │   ├── test_players.py
#### │   └── test_teams.py
#### ├── .gitignore
#### ├── alembic.ini
#### ├── database.db
#### |── README.md
#### └── requirements.txt
