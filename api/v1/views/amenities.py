#!/usr/bin/python3
"""
Flask Amenity blueprint importation
"""
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity

@app_views.route('/amenities', methods=['GET'])
def get_all_amenities():
    """Retrieve the list of all Amenity objects"""
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])

@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity_by_id(amenity_id):
    """Retrieve an Amenity object by ID"""
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(amenity_obj.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Delete an Amenity object by ID"""
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        return jsonify({"error": "Not found"}), 404

    storage.delete(amenity_obj)
    storage.save()
    return jsonify({}), 200

@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """Create an Amenity object"""
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json()
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201

@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Update an Amenity object by ID"""
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        return jsonify({"error": "Not found"}), 404

    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json()

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity_obj, key, value)

    storage.save()
    return jsonify(amenity_obj.to_dict()), 200
