#!/usr/bin/python3
"""handles all default RESTFul API actions"""
from . import app_views
from models.user import User
from flask import jsonify, abort, request, make_response
from models import storage


@app_views.route(
        '/users',
        methods=['GET'],
        strict_slashes=False
    )
def list_users():
    """Retrieves the list of all Users"""
    return jsonify(
            [obj.to_dict() for obj in storage.all(User).values()])


@app_views.route(
        '/users/<string:user_id>',
        methods=['GET']
    )
def get_user(user_id):
    """Retrieves a User object"""

    user = storage.get(User, user_id)

    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route(
        '/users/<user_id>',
        methods=['DELETE'],
        strict_slashes=False
    )
def delete_user(user_id):
    """Deletes a user"""

    user = storage.get(User, user_id)

    if not user:
        abort(404)

    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/users',
        methods=['POST'],
        strict_slashes=False
    )
def create_user():
    """Creates a user"""
    json_body = request.get_json()

    if not json_body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'email' not in json_body:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if 'password' not in json_body:
        return make_response(jsonify({"error": "Missing pasword"}), 400)

    user = User(**json_body)
    user.save()

    return jsonify(user.to_dict()), 201


@app_views.route(
        '/users/<string:user_id>',
        methods=['PUT'],
        strict_slashes=False
    )
def update_user(user_id):
    """Updates a User object"""

    user = storage.get(User, user_id)

    if not user:
        abort(404)

    json_body = request.get_json()

    if not json_body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for k, v in json_body.items():
        if k not in ['id', 'email', 'created_at', 'updated']:
            setattr(user, k, v)

    storage.save()

    return jsonify(user.to_dict()), 200
