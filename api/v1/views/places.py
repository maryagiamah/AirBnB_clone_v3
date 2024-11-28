#!/usr/bin/python3
"""handles all default RESTFul API actions"""
from . import app_views
from models.place import Place
from models.city import City
from models.user import User
from flask import jsonify, abort, request
from models import storage


@app_views.route(
        '/cities/<string:city_id>/places',
        methods=['GET'],
        strict_slashes=False
    )
def list_places(city_id):
    """Retrieves the list of all Places"""

    city = storage.get(City, city_id)

    if not city:
        abort(404)

    places = [
            obj.to_dict() for obj in storage.all(Place).values()
            if obj.city_id == city_id
        ]

    return jsonify(places)


@app_views.route(
        '/places/<string:place_id>',
        methods=['GET']
    )
def get_place(place_id):
    """Retrieves a Place object"""

    place = storage.get(Place, place_id)

    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
        '/places/<place_id>',
        methods=['DELETE'],
        strict_slashes=False
    )
def delete_place(place_id):
    """Deletes a Place"""

    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/cities/<string:city_id>/places',
        methods=['POST'],
        strict_slashes=False
    )
def create_place(city_id):
    """Creates a Place"""

    city = storage.get(City, city_id)

    if not city:
        abort(404)

    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    json_body = request.get_json()

    if 'user_id' not in json_body:
        return jsonify({"error": "Missing user_id"}), 400
    if not storage.get(User, json_body.get('user_id')):
        abort(404)

    if 'name' not in json_body:
        return jsonify({"error": "Missing name"}), 400

    place = Place(**json_body)
    place.save()

    return jsonify(place.to_dict()), 201


@app_views.route(
        '/places/<string:place_id>',
        methods=['PUT'],
        strict_slashes=False
    )
def update_place(place_id):
    """Updates a Place object"""

    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    json_body = request.get_json()

    for k, v in json_body.items():
        if k not in ['id', 'user_id', 'city_id', 'created_at', 'updated']:
            setattr(place, k, v)

    storage.save()

    return jsonify(place.to_dict()), 200
