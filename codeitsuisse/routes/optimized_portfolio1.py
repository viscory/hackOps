import logging
import json
from flask import request, jsonify
from codeitsuisse import app
from math import inf

logger = logging.getLogger(__name__)

@app.route('/optimizedportfolio', methods=['POST'])
def optimizer():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    print(data)
    inputs = data.get("inputs")
    temp = dict()
    temp['outputs'] = portfolioOpt(inputs)
    return jsonify(temp)

def portfolioOpt(inputs):
    result = []
    for dict1 in inputs:
        pValue, sVol = dict1["Portfolio"]["Value"], dict1["Portfolio"]["SpotPrcVol"]
        futures = dict1["IndexFutures"]
        ohr, fpVol, numFC = inf, inf, inf
        for future in futures:
            fpVol_cal = future['FuturePrcVol']
            ohr_cal = round((future["CoRelationCoefficient"]
                       * sVol) / future['FuturePrcVol'], 3)
            numFC_cal = int((ohr_cal) * (pValue /
                         (future['IndexFuturePrice'] * future['Notional'])) + 0.5)
            if ohr_cal < ohr and fpVol_cal < fpVol:
                fut_name=future["Name"]
                ohr, fpVol, numFC=ohr_cal, fpVol_cal, numFC_cal
            elif (ohr_cal == ohr and fpVol_cal == fpVol) or (ohr_cal < ohr and fpVol > fpVol_cal) or (ohr_cal > ohr and fpVol < fpVol_cal):
                if numFC_cal < numFC:
                    numFC = numFC_cal
                    fut_name = future["Name"]
        output = {"HedgePositionName": fut_name, "OptimalHedgeRatio": ohr,
                "NumFuturesContract": numFC }
        result.append(output)
    return result
