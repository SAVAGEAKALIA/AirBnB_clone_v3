#!/usr/bin/python3
"""
Flask Place blueprint importation
"""
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User

@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places_by_city(city_id):
    """Retrieve the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404

    places = storage.all(Place).values()
    city_places = [place.to_dict() for place in places if place.city_id == city_id]
    return jsonify(city_places)

@app_views.route('/places/<place_id>', methods=['GET'])
def get_place_by_id(place_id):
    """Retrieve a Place object by ID"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(place.to_dict())

@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Delete a Place object by ID"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404

    storage.delete(place)
    storage.save()
    return jsonify({}), 200

@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Create a Place object"""
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404

    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json()
    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get(User, data['user_id'])
    if user is None:
        return jsonify({"error": "Not found"}), 404
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    new_place = Place(**data)
    new_place.city_id = city_id
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201

@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Update a Place object by ID"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404

    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json()

    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200
