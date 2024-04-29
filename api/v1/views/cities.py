#!/usr/bin/python3
"""flask view for the city class"""
from models.state import City
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Gets the city data with the city ID"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    return city, 200
        
@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    result = []
    city = storage.all('City')
    for key in city:
        if city[key].state_id == state_id:
            result.append(city[key])
    return jsonify(result), 200