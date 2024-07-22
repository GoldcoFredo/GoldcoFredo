#!/bin/bash

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Run the application using Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 Conexion:app
