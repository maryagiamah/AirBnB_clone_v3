#!/usr/bin/python3
"""handles all default RESTFul API actions"""
from . import app_views
from models.place import Place
from models.review import Review
from models.user import User
from flask import jsonify, abort, request
from models import storage


@app_views.route(
        '/places/<string:place_id>/reviews',
        methods=['GET'],
        strict_slashes=False
    )
def list_reviews(place_id):
    """Retrieves the list of all Reviews"""

    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    reviews = [
            obj.to_dict() for obj in storage.all(Review).values()
            if obj.place_id == place_id
        ]

    return jsonify(reviews)


@app_views.route(
        '/reviews/<string:review_id>',
        methods=['GET']
    )
def get_review(review_id):
    """Retrieves a Review object"""

    review = storage.get(Review, review_id)

    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
        '/reviews/<review_id>',
        methods=['DELETE'],
        strict_slashes=False
    )
def delete_review(review_id):
    """Deletes a Review"""

    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/places/<string:place_id>/reviews',
        methods=['POST'],
        strict_slashes=False
    )
def create_review(place_id):
    """Creates a Review"""

    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    try:
        json_body = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    if 'user_id' not in json_body:
        return jsonify({"error": "Missing user_id"}), 400
    if not storage.get(User, json_body.get('user_id')):
        abort(404)

    if 'text' not in json_body:
        return jsonify({"error": "Missing text"}), 400

    review = Review(**json_body)
    review.save()

    return jsonify(review.to_dict()), 201


@app_views.route(
        '/reviews/<string:review_id>',
        methods=['PUT'],
        strict_slashes=False
    )
def update_review(review_id):
    """Updates a Review object"""

    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    try:
        json_body = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    for k, v in json_body.items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated']:
            setattr(review, k, v)

    storage.save()

    return jsonify(review.to_dict()), 200
