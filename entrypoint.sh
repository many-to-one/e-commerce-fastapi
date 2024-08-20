#!/bin/bash

export DATABASE_URL=${DATABASE_URL}

# db:5432 --timeout=30 -- echo "PostgreSQL is up - executing command"

# Check if alembic.ini exists, if not, initialize alembic
if [ ! -f "alembic.ini" ]; then
    echo "Initializing Alembic..."
    # alembic init alembic #synchronouse
    alembic init -t async alembic #asynchronouse
fi

# Set up the database (e.g., run migrations)
# alembic revision --autogenerate -m "add: categories logic"
# alembic upgrade head

# Use once at first time, than add secret_key to .env and delete secret.txt
# python generate_secret_key.py > secret.txt 

# Start the FastAPI server
exec uvicorn main:app --reload --host 0.0.0.0 --port 8000