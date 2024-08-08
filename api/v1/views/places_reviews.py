#!/usr/bin/python3
"""
Flask Review blueprint importation
"""
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User

@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews_by_place(place_id):
    """Retrieve the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404

    reviews = storage.all(Review).values()
    place_reviews = [review.to_dict() for review in reviews if review.place_id == place_id]
    return jsonify(place_reviews)

@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review_by_id(review_id):
    """Retrieve a Review object by ID"""
    review = storage.get(Review, review_id)
    if review is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(review.to_dict())

@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Delete a Review object by ID"""
    review = storage.get(Review, review_id)
    if review is None:
        return jsonify({"error": "Not found"}), 404

    storage.delete(review)
    storage.save()
    return jsonify({}), 200

@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """Create a Review object"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404

    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json()
    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get(User, data['user_id'])
    if user is None:
        return jsonify({"error": "Not found"}), 404
    if 'text' not in data:
        return jsonify({"error": "Missing text"}), 400

    new_review = Review(**data)
    new_review.place_id = place_id
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201

@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """Update a Review object by ID"""
    review = storage.get(Review, review_id)
    if review is None:
        return jsonify({"error": "Not found"}), 404

    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json()

    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)

    storage.save()
    return jsonify(review.to_dict()), 200
