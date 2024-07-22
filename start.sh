#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run the Flask application using Flask CLI
flask run --host=0.0.0.0 --port=8080
