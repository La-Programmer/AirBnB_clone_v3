#!/usr/bin/python3

from models.amenity import Amenity
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views

@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Gets a list of all amenities in DB"""
    amenities = storage.all('Amenity')
    result = []
    for key, value in amenities.items():
        result.append(value.to_dict())
    return jsonify(result)

@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Gets an amenity of the given id"""
    amenity = storage.get('Amenity', amenity_id)
    if not amenity:
        abort(404)
    else:
        return jsonify(amenity.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete the amenity with the given id"""
    amenity = storage.get('Amenity', amenity_id)
    if not amenity:
        abort(404)
    else:
        amenity.delete()
        storage.save()
        return jsonify({}), 200

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a new amenity object"""
    if not request.json:
        return(jsonify({"error": "Not a JSON"})), 400
    elif 'name' not in request.json:
        return(jsonify({"error": "Missing name"})), 400
    else:
        data = request.get_json()
        new_amenity = Amenity(**data)
        new_amenity.save()
        return new_amenity.to_dict(), 201

@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates a amenity object in DB"""
    ignore_keys = ['id', 'created_at', 'updated_at']
    amenity = storage.get('Amenity', amenity_id)
    if not amenity:
        abort(404)
    elif not request.json:
        return(jsonify({"error": "Not a JSON"})), 400
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
