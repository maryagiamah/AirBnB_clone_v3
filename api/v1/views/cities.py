#!/usr/bin/python3
"""handles all default RESTFul API actions"""
from . import app_views
from models.state import State
from models.city import City
from flask import jsonify, abort, request
from models import storage


@app_views.route(
        '/states/<string:state_id>/cities',
        methods=['GET'],
        strict_slashes=False
    )
def list_cities(state_id):
    """Retrieves the list of all Cities"""

    state = storage.get(State, state_id)

    if not state:
        abort(404)

    cities = [
            obj.to_dict() for obj in storage.all(City).values()
            if obj.state_id == state_id
        ]

    return jsonify(cities)


@app_views.route(
        '/cities/<string:city_id>',
        methods=['GET']
    )
def get_city(city_id):
    """Retrieves a City object"""

    city = storage.get(City, city_id)

    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route(
        '/cities/<city_id>',
        methods=['DELETE'],
        strict_slashes=False
    )
def delete_city(city_id):
    """Deletes a city"""

    city = storage.get(City, city_id)

    if not city:
        abort(404)

    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/states/<string:state_id>/cities',
        methods=['POST'],
        strict_slashes=False
    )
def create_city(state_id):
    """Creates a city"""

    state = storage.get(State, state_id)

    if not state:
        abort(404)

    try:
        json_body = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    if 'name' not in json_body:
        return jsonify({"error": "Missing name"}), 400

    json_body["state_id"] = state_id
    city = City(**json_body)
    city.save()

    return jsonify(city.to_dict()), 201


@app_views.route(
        '/cities/<string:city_id>',
        methods=['PUT'],
        strict_slashes=False
    )
def update_city(city_id):
    """Updates a City object"""

    city = storage.get(City, city_id)

    if not city:
        abort(404)

    try:
        json_body = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    for k, v in json_body.items():
        if k not in ['id', 'state_id', 'created_at', 'updated']:
            setattr(city, k, v)

    storage.save()

    return jsonify(city.to_dict()), 200
