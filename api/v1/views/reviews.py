#!/usr/bin/python3

from models.review import Review
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'],
                 strict_slashes=False)
def get_reviews_in_places(place_id):
    """Gets a list of all the reviews in a place"""
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    else:
        reviews = storage.all('Review')
        result = []
        for key in reviews:
            if reviews[key].place_id == place_id:
                result.append(reviews[key].to_dict())
        return jsonify(result), 201


@app_views.route('/reviews/<review_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Gets a review by ID"""
    review = storage.get('Review', review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a review by ID"""
    review = storage.get('Review', review_id)
    if not review:
        abort(404)
    else:
        review.delete()
        storage.save()
        return {}, 201


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a review in place of place_id"""
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    elif not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()
    if "user_id" not in data:
        return jsonify({"error": "Missing user_id"})
    elif "text" not in data:
        return jsonify({"error": "Missing text"})
    else:
        user = storage.get('User', data["user_id"])
        if not user:
            abort(404)
        review = Review(**data, place_id=place_id)
        review.save()
        return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Updates review by ID"""
    review = storage.get('Review', review_id)
    if not review:
        abort(404)
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    else:
        data = request.get_json()
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
