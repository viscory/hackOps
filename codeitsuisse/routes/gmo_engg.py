<<<<<<< HEAD
=======
from collections import Counter 

>>>>>>> a3b3f8b7ae0c88bd3404b4222e4f8c200026bf0d
import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/intelligent-farming', methods=['POST'])
<<<<<<< HEAD
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
               
=======
def evaluateGMO():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    runId = data.get("runId")
    list = data.get("list")
    ans = []

    for item in list:
        seq = item["geneSequence"]
        result = gmo(seq)

        ans.append({"id":item["id"], "geneSequence":result})    

    result = {"runId":runId, "list":ans}
    logging.info("My result :{}".format(result))
    return jsonify(result)

def gmo(seq):

    characterCount = Counter(seq)
    sequence = []
    cc_count = 0
    acgt_count = 0

    while characterCount["C"] > 1:
        sequence.append("CC")
        characterCount["C"] -= 2
        cc_count += 1

    while characterCount["A"] > 0 and characterCount["C"] > 0 and characterCount["G"] > 0 and characterCount["T"] > 0:
        sequence.append("ACGT")
        characterCount["A"] -= 1
        characterCount["C"] -= 1
        characterCount["G"] -= 1
        characterCount["T"] -= 1
        acgt_count += 1

    for k,v in characterCount.items():
        if k != "A":
            for i in range(v):
                sequence.append(k)

    for count in range(cc_count):

        if characterCount["A"] > 1:

            sequence.insert(count*2, "AA")
            characterCount["A"] -= 2

        elif characterCount["A"] == 1:

            sequence.insert(count*2, "A")
            characterCount["A"] -= 1


    for count in range(acgt_count):

        if characterCount["A"] > 0:

            sequence.insert(cc_count*2 + count*2, "A")
            characterCount["A"] -= 1

    count = 0

    while characterCount["A"] > 0:

        if characterCount["A"] == 1:
            sequence.insert(cc_count*2 + acgt_count*2 + count*2, "A")
            characterCount["A"] -= 1

        else:
            sequence.insert(cc_count*2 + acgt_count*2 + count*2, "AA")
            characterCount["A"] -= 2
        count += 1

    return "".join(sequence)
>>>>>>> a3b3f8b7ae0c88bd3404b4222e4f8c200026bf0d
