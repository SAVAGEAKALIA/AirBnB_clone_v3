#!/usr/bin/python3
"""
Flask state blueprint importation
"""
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('states', methods=['GET'])
def get_all_states():
    """Returns all states objects"""
    states = storage.all(State)
    return jsonify([stat.to_dict() for stat in states.values()])


@app_views.route('states/<state_id>', methods=['GET'])
def get_state_by_id(state_id):
    """return state obj bid"""
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        return jsonify({"error": "Not found"}), 404
    return state_obj.to_dict()


@app_views.route('states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """delete state obj by id"""
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(state_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    """Creates a State object"""
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json()  # Retrieve the JSON data as a dictionary
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """update state obj by id"""
    state_obj = storage.get(State, state_id)

    if state_obj is None:
        return jsonify({"error": "Not found"}), 404

    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    state_obj_dict = request.get_json()

    for key, value in state_obj_dict.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state_obj, key, value)

    storage.save()
    return jsonify(state_obj.to_dict()), 200
