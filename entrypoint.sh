#!/bin/bash

export DATABASE_URL=${DATABASE_URL}

# db:5432 --timeout=30 -- echo "PostgreSQL is up - executing command"

# Check if alembic.ini exists, if not, initialize alembic
if [ ! -f "alembic.ini" ]; then
    echo "Initializing Alembic..."
    alembic init alembic
fi

# Set up the database (e.g., run migrations)
alembic revision --autogenerate -m "add is_admin to users table"
alembic upgrade head

# Start the FastAPI server
exec uvicorn main:app --reload --host 0.0.0.0 --port 8000