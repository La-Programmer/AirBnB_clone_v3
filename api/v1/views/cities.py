#!/usr/bin/python3
"""flask view for the city class"""
from models.city import City
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """gets all the cities in a state"""
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    result = []
    city = storage.all('City')
    for key in city:
        if city[key].state_id == state_id:
            result.append(city[key].to_dict())
    return jsonify(result), 200

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Gets the city data with the city ID"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict()), 200

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Delete a city by ID"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return {}, 200

@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Creates a new city with data from the POST Method"""
    if not request.json:
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'name' not in request.json:
        return jsonify({'error': 'Missing name'}), 400
    else:
        data = request.get_json()
        new_city = City(**data, state_id=state_id)
        new_city.save()
        return jsonify(new_city.to_dict()), 201
    
@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates the city instance with data from PUT method"""
    city_obj = storage.get('City', city_id)
    if not city_obj:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    ignore = ['id', 'state_id', 'created_at', 'updated_at']
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(city_obj, key, value)
    city_obj.save()
    return jsonify(city_obj.to_dict()), 200
