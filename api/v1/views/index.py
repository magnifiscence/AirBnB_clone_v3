#!/usr/bin/python3
"""
Creates a route /status on the object app_views that returns a JSON status
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """Returns a JSON status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """Returns a JSON stats"""
    classes = {"Amenity": "amenities", "City": "cities",
               "Place": "places", "Review": "reviews",
               "State": "states", "User": "users"}
    new_dict = {}
    for k, v in classes.items():
        new_dict[v] = storage.count(k)
    return jsonify(new_dict)
