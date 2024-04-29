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
    new_state = []
    new_state.append(city)
    return new_state, 200
        
@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_city(state_id):
    city = storage.get('City', state_id)          