#!/usr/bin/python3
"""Starts a Flask web application"""
import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(self):
    """Closes the storage"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Handler for 404 error"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
