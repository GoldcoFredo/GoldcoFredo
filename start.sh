#!/bin/bash

set -e

# Upgrade pip if necessary
pip install --upgrade pip

# Install dependencies if not already installed
if [ ! -f ./.venv/lib/python3.11/site-packages/snowflake_connector_python ]; then
  pip install -r requirements.txt
fi

# Run the application using Gunicorn with more efficient worker settings
gunicorn -w 2 -b 0.0.0.0:8000 Conexion:app --log-level=info --access-logfile=- --error-logfile=-
