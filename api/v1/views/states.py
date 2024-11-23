#!/usr/bin/python3
"""handles all default RESTFul API actions"""
from . import app_views
from models.state import State
from flask import jsonify, abort, request, make_response
from models import storage


@app_views.route(
        '/states',
        methods=['GET'],
        strict_slashes=False
    )
def list_states():
    """Retrieves the list of all State"""
    return jsonify(
            [obj.to_dict() for obj in storage.all(State).values()])


@app_views.route(
        '/states/<string:state_id>',
        methods=['GET']
    )
def get_state(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id)

    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route(
        '/states/<state_id>',
        methods=['DELETE'],
        strict_slashes=False
    )
def delete_state(state_id):
    """Deletes a state"""
    state = storage.get(State, state_id)

    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route(
        '/states',
        methods=['POST'],
        strict_slashes=False
    )
def create_state():
    """Creates a state"""
    json_body = request.get_json()

    if not json_body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in json_body:
        return make_response(jsonify({"error": "Missing name"}), 400)

    state = State(**json_body)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route(
        '/states/<string:state_id>',
        methods=['PUT'],
        strict_slashes=False
    )
def update_state(state_id):
    """Updates a State object"""

    json_body = request.get_json()

    if not json_body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    for k, v in json_body.items():
        if k not in ['id', 'created_at', 'updated']:
            setattr(state, k, v)

    storage.save()

    return jsonify(state.to_dict()), 200
