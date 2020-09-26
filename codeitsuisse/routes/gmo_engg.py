import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/intelligent-farming', methods=['POST'])
def farmer():
    data = request.get_json()
    response = data
    genDict = {'A':0, 'C':0, 'T':0, 'G':0}
    for index, gene in enumerate(data.get('list')):
        sequence = gene.get('geneSequence')
        for char in sequence:
            genDict[char] += 1
        response['list'][index]['geneCount'] = genDict
    print(response)
    return response
               
