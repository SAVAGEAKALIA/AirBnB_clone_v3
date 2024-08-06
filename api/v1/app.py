#!/usr/bin/python3
"""
Flask configuration for Api
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Returns 404 error"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    HBNB_API_HOST = os.getenv('HBNB_API_HOST', '0.0.0.0')
    HBNB_API_PORT = int(os.getenv('HBNB_API_PORT', '5000'))

    app.run(host=HBNB_API_HOST, port=int(HBNB_API_PORT), threaded=True, debug=True)
