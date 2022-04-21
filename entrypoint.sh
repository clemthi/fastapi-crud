#! /usr/bin/env bash

set -e

# Load config param form dotenv file
if [[ -f "$PWD/.env" ]]; then
  export $(cat .env | xargs)
fi

# Create database schema using alembic
alembic upgrade head

# Inject initial data in DB
python -m app.set_db

# Start uvicorn server
uvicorn app.main:app --host 0.0.0.0 --port 8080
