#!/usr/bin/python3
"""
Flask state blueprint importation
"""
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models import state


@app_views.route('states', methods=['GET'])
def get_all_states():
    """Returns all states objects"""
    states = storage.all(state)
    return storage.to_dict(states)


@app_views.route('states/<state_id>', methods=['GET'])
def get_state_by_id(state_id):
    """return state obj bid"""
    state_obj = storage.get(state, state_id)
    if state_obj is None:
        return jsonify({"error": "Not found"}), 404
    return state_obj.to_dict()


@app_views.route('states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """delete state obj by id"""
    state_obj = storage.get(state, state_id)
    if state_obj is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(state_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('states', methods=['POST'])
def create_state():
    """create new state obj"""
    new_state = storage.new(state)
    new_state.name = request.json.get('name')
    if new_state.name is None:
        return jsonify({"error": "Missing name"}), 400
    elif new_state.name is not jsonify(new_state.name):
        return jsonify({"Not a JSON"}), 400
    else:
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """update state obj by id"""
    state_obj = storage.get(state, state_id)

    if state_obj is None:
        return jsonify({"error": "Not found"}), 404

    state_obj_dict = request.get_json(state_obj)

    if state_obj_dict is not jsonify(state_obj):
        return jsonify({"error": "Not a json"}), 400
    elif request.json.get('name') is not None:
        state_obj.name = request.json.get('name')
    storage.save()
    return jsonify(state_obj.to_dict()), 200
