#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run the Flask application using Flask CLI and default Render port
flask run --host=0.0.0.0 --port=${PORT:-10000}
