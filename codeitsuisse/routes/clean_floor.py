import math
import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/clean_floor', methods=['POST'])
def clean_floor():
    data = request.get_json()
    result = dict()
    result['answers'] = CleanFloor(data.get('tests'))
    return jsonify(result)



def CleanFloor(tests):	
    result = {}
    print(tests)
    for keys, values in tests.items():
        print(values)
        values = values['floor']
        counter = 0
        sum1 = sum(values)
        for i in range(1, len(values)):
            if sum1 == 0:
                break
            counter += 1
            if values[i] == 0:
                values[i] += 1
                sum1 += 1
            else:
                values[i] -= 1
                sum1 -= 1
            if values[i - 1] != 0:
                sum1 -= values[i - 1]
                counter += 2 * values[i - 1] - 1
                if (values[i] < values[i - 1] - 1):
                    temp = values[i - 1] - 1 - values[i]
                    if (temp % 2 == 0):
                        sum1 -= values[i]
                        values[i] = 0
                    else:
                        sum1 -= values[i] - 1
                        values[i] = 1
                else:
                    sum1 -= values[i - 1] - 1
                    values[i] -= values[i - 1] - 1
                values[i - 1] = 0
                if sum1 == 0:
                    break

                counter += 1
                if values[i] == 0:
                    values[i] += 1
                    sum1 += 1
                else:
                    values[i] -= 1
                    sum1 -= 1
        if sum1 != 0:
            temp = values[len(values) - 1]
            counter += 2 * temp
            if (temp % 2 == 1):
                counter += 1
        result[keys] = counter
    return result
