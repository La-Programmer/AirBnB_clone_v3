#!/usr/bin/python3
"""Returns the status of the API"""

from flask import Flask
from models import storage
from os import getenv
from api.v1.views import app_views


app = Flask(__name__)
@app.register_blueprint(app_views)
@app.teardown_appcontext
def reload_session(exception):
    """Reload the DB session"""
    storage.close()

if __name__ == '__main__':
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if host is None:
        host = '0.0.0.0'
    if port is None:
        port = '5000'
    app.run(debug=True, host=host, port=port, threaded=True)
