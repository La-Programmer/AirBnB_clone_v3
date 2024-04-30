#!/usr/bin/python3

from models.place import Place
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views

@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places_in_cities(city_id):
    """Gets a list of all the places in a city"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    else:
        places = storage.all('Place')
        result = []
        for key in places:
            if places[key].city_id == city_id:
                result.append(places[key].to_dict())
        return jsonify(result), 201

@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Gets a place by ID"""
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict()), 201

@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a place by ID"""
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    else:
        place.delete()
        storage.save()
        return {}, 201

@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a place in city of city_id"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    elif not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()
    if "user_id" not in data:
        return jsonify({"error": "Missing user_id"})
    elif "name" not in data:
        return jsonify({"error": "Missing name"})
    else:
        user = storage.get('User', data["user_id"])
        if not user:
            abort(404)
        place = Place(**data, city_id=city_id)
        place.save()
        return jsonify(place.to_dict()), 201

@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates place by ID"""
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    else:
        data = request.get_json()
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(place, key, value)
    return jsonify(place.to_dict()), 200
