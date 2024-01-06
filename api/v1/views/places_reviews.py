#!/usr/bin/python3
"""This module creates a new view for place objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.place import Place
from models.state import State


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all place objects"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = city.places
    return jsonify([place.to_dict() for place in places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a place object"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    place = storage.get(City, city_id)
    if not place:
        abort(404)
    place = request.get_json()
    if not place:
        abort(400, description="Not a JSON")
    if 'user_id' not in place:
        abort(400, description="Missing user_id")
    if 'name' not in place:
        abort(400, description="Missing name")
    place = Place(city_id=city.id, **place)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place_json = request.get_json()
    if not place_json:
        abort(400, description="Not a JSON")
    place.name = place_json.get('name', place.name)
    place.save()
    return jsonify(place.to_dict()), 200
