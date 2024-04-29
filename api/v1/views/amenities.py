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
