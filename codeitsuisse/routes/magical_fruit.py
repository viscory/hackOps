import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/fruitbasket', methods=['POST'])
def magicFruits():
    temDict = dict()
    guess = 0
    keyDict = {
        'maPomegranate': 65,
        'maPineapple': 65,
        'maApple': 50,
        'maWatermelon': 35,
        'maRambutan': 50,
        'maAvocado': 40
    }
    data = str(request.data)[3:-2].split(',')
    print(data)
    for x in data:
        x = x.split(':')
        print(x)
        temDict[x[0][1:-1]] = int(x[1])
    for key in temDict.keys():
        try:
            guess += tempDict[key] * keyDict[key]
        except:
            pass
           
    print(guess)
    print(keyDict)
    return jsonify(guess)


def magicalBasket(dict1):
    print(10000)
