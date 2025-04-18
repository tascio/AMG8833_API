from flask import Blueprint, current_app, jsonify
from main import rts
import random, time


api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/temperature', methods=['POST'])
def write_temperature():
    keys = ['t_max', 't_thermistor'] + [
        f'array{row}{col}' for row in range(8) for col in range(8)
    ]

    result = {}

    for key in keys:
        try:
            data_point = rts.get(key)
            if data_point:
                timestamp, value = data_point
                result[key] = {
                    'timestamp': timestamp,
                    'value': value
                }
        except Exception as e:
            result[key] = {'error': str(e)}

    return jsonify(result)