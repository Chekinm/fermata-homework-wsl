"""
Flask Application Launcher

This script serves as the entry point for running the Flask application.

To run the Flask application:

- set FLASK_APP environment variable to run.py
    export FLASK_APP=run.py
- run flask with
    flask run
    
"""

from app import app
from config.config import FLASK_DEBUG, FLASK_HOST

if __name__ == "__main__":
    app.run(host=FLASK_HOST, debug=FLASK_DEBUG)
