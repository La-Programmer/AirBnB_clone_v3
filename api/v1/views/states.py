#!/usr/bin/python3
"""Flask view for the State class"""

from models.state import State
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Gets a list of all states in DB"""
    states = storage.all('State')
    result = []
    for key, value in states.items():
        result.append(value.to_dict())
    return jsonify(result)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Gets a state of the given id"""
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    else:
        return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Delete the state with the given id"""
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    else:
        state.delete()
        storage.save()
        return jsonify({}), 200

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new state object"""
    if not request.json:
        return(jsonify({"error": "Not a JSON"})), 400
    elif 'name' not in request.json:
        return(jsonify({"error": "Missing name"})), 400
    else:
        data = request.get_json()
        new_state = State(**data)
        new_state.save()
        return new_state.to_dict(), 201

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a state object in DB"""
    ignore_keys = ['id', 'created_at', 'updated_at']
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    elif not request.json:
        return(jsonify({"error": "Not a JSON"})), 400
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
