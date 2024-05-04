#!/usr/bin/python3
"""This module is the base api file for the app"""

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
    keys = ['amenities', 'cities', 'places', 'reviews', 'states', 'users']
    stat_obj = {}
    index = 0
    for key in classes:
        stat_obj[keys[index]] = storage.count(key)
        index += 1
    return jsonify(stat_obj)
