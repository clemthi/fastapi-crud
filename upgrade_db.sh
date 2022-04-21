#! /usr/bin/env bash

set -e
set -x

# Load config param form dotenv file
if [[ -f "$PWD/.env" ]]; then
  export $(cat .env | xargs)
fi

# Create database schema using alembic
alembic upgrade head

# Inject initial data in DB
python -m app.set_db
