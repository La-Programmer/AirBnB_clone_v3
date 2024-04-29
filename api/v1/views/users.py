#!/usr/bin/python3

from models.user import User
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Gets a list of all users in DB"""
    users = storage.all('User')
    result = []
    for key, value in users.items():
        result.append(value.to_dict())
    return jsonify(result)

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Gets a user of the given id"""
    user = storage.get('User', user_id)
    if not user:
        abort(404)
    else:
        return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete the user with the given id"""
    user = storage.get('User', user_id)
    if not user:
        abort(404)
    else:
        user.delete()
        storage.save()
        return jsonify({}), 200

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a new user object"""
    if not request.json:
        return(jsonify({"error": "Not a JSON"})), 400
    elif 'email' not in request.json:
        return(jsonify({"error": "Missing email"})), 400
    elif 'password' not in request.json:
        return(jsonify({"error": "Missing password"})), 400
    else:
        data = request.get_json()
        new_user = User(**data)
        new_user.save()
        return new_user.to_dict(), 201

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a user object in DB"""
    ignore_keys = ['id', 'created_at', 'updated_at']
    user = storage.get('User', user_id)
    if not user:
        abort(404)
    elif not request.json:
        return(jsonify({"error": "Not a JSON"})), 400
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
