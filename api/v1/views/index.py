#!/usr/bin/python3

from flask import jsonify
from models import storage
from models.engine.db_storage import classes
from api.v1.views import app_views

@app_views.route('/status')
def status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"})

@app_views.route('/stats')
def stats():
    """Retrieves the number of each object by type"""
    stat_obj = {}
    for key in classes:
        stat_obj[key] = storage.count(key)
    return jsonify(stat_obj)
