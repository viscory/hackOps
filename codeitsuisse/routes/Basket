import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;
from itertools import combinations
import numpy
import ast

logger = logging.getLogger(__name__)

@app.route('/fruitbasket', methods=['POST'])
def evaluateMagicBasketWeight():
    data = request.get_data()
    logging.info("data sent for evaluation {}".format(data))

    dict_str = data.decode("UTF-8")
    print(type(dict_str))

    fruit1 = dict_str[dict_str.find(":") + 1 : dict_str.find(",")]
    firstColon = dict_str.find(":") + 1
    firstComma = dict_str.find(",") + 1
    fruit2 = dict_str[dict_str.find(":", firstColon)+1 : dict_str.find(",", firstComma)]
    secondColon = dict_str.find(":", firstColon) + 1
    fruit3 = dict_str[dict_str.find(":", secondColon)+1 : dict_str.find("}")]

    print(fruit1, fruit2, fruit3)

    fruit1 = int(fruit1)
    fruit2 = int(fruit2)
    fruit3 = int(fruit3)

    result = fruit1 * 20 + fruit2 * 15 + fruit3 * 20

    logging.info("My result :{}".format(result))
    return str(result)
