from flask import Blueprint, current_app, jsonify
from main import rts
import random, time


api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/get_tmax', methods=['POST'])
def get_tmax():
    return jsonify({'t_max' : rts.get('t_max')[1]})  #timestamp, value

@api_blueprint.route('/get_tthermistor', methods=['POST'])
def get_tthermistor():
    return jsonify({'t_thermistor' : rts.get('t_thermistor')[1]})

@api_blueprint.route('/get_tarray', methods=['POST'])
def get_tarray():
    keys = [f'array{row}{col}' for row in range(8) for col in range(8)]
    array = {}

    for key in keys:
        p_array_val = rts.get(key)[1]
        array[key] = p_array_val

    return jsonify(array)