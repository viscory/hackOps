import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/salad-spree', methods=['POST'])
def calculateprice():
    data = request.get_json()
    print(data)
    n = data.get("number_of_salads")
    streets = data.get("salad_prices_street_map")
    costs = []
    result = 0
    
    for street in streets:
        for i in range(0,len(street)-n+1):
            consecutive = street[i:i+n]
            if "X" not in consecutive:
                consecutive[:] = list(map(int, consecutive))
                costs.append(sum(consecutive))
    if costs:
        result = min(costs)

    returndict = {"result" : result}
    return jsonify(returndict)    
