#!/usr/bin/python3
"""
Flask City blueprint importation
"""
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State

@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities_by_state(state_id):
    """Retrieve the list of all City objects of a State"""
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        return jsonify({"error": "Not found"}), 404

    cities = storage.all(City).values()
    state_cities = [city.to_dict() for city in cities if city.state_id == state_id]
    return jsonify(state_cities)

@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city_by_id(city_id):
    """Retrieve a City object"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(city_obj.to_dict())

@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Delete a City object"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        return jsonify({"error": "Not found"}), 404

    storage.delete(city_obj)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Create a City object"""
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        return jsonify({"error": "Not found"}), 404

    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json()
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    new_city = City(**data)
    new_city.state_id = state_id
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201

@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Update a City object"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        return jsonify({"error": "Not found"}), 404

    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json()

    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city_obj, key, value)

    storage.save()
    return jsonify(city_obj.to_dict()), 200
