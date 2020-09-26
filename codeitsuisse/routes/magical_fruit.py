import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/fruitbasket', methods=['POST'])
def magicFruits():
    temDict = dict()
    keyDict = {
        'maPomegranate': 50,
        'maPineapple': 50,
        'maApple': 50,
        'maWatermelon': 50,
        'maRangutan': 50
    }
    data = str(request.data)
    print(data)
    for x in data[3:-2].split(','):
        x.split(':')
        temDict[x[0]] = int(x[1])
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
