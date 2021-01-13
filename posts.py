from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request

def create_data(data):

    if not request.json or not 'name' in request.json:
        abort(400)
    # TODO: Make a schema for data to add to main data list
    added = {
        'id': data[-1]['id'] + 1,
        'name': request.json['name'],
        'breed': request.json.get('breed'," "),
        'age': request.json.get('age')
    }
    # Append to main data list
    data.append(added)
    return jsonify({'data': added}), 201